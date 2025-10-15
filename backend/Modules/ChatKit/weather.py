from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Literal, Sequence
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import httpx

from .sample_widget import HourlyForecast, WeatherWidgetData

USER_AGENT = "ChatKitWeatherTool/1.0 (+https://openai.com/)"
DEBUG_PREFIX = "[WeatherDebug]"
GEOCODE_URL = "https://nominatim.openstreetmap.org/search"
OPEN_METEO_GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
CURRENT_FIELDS = (
    "temperature_2m,apparent_temperature,relative_humidity_2m,"
    "is_day,wind_speed_10m,wind_direction_10m,weather_code"
)
HOURLY_FIELDS = "temperature_2m,weather_code"
DAILY_FIELDS = (
    "weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,"
    "precipitation_probability_max"
)
DEFAULT_TIMEOUT = 20.0
HOURLY_SEGMENTS = 6


class WeatherLookupError(RuntimeError):
    """Raised when the weather service could not satisfy a request."""


def _debug(message: str, *, extra: dict[str, Any] | None = None) -> None:
    payload = f"{DEBUG_PREFIX} {message}"
    if extra:
        payload = f"{payload} | {extra}"
    print(payload)


@dataclass(frozen=True)
class GeocodedLocation:
    latitude: float
    longitude: float
    label: str
    raw: dict[str, Any]


WEATHER_CODE_LOOKUP: dict[int, tuple[str, str]] = {}

DEFAULT_ICON_KEY = "cloud"


def _register_weather_codes(codes: Sequence[int], label: str, icon: str) -> None:
    for code in codes:
        WEATHER_CODE_LOOKUP[int(code)] = (label, icon)


_register_weather_codes([0], "Clear sky", "sun")
_register_weather_codes([1], "Mostly sunny", "cloud-sun")
_register_weather_codes([2], "Partly cloudy", "cloud-sun")
_register_weather_codes([3], "Overcast", "cloud")
_register_weather_codes([45, 48], "Foggy", "cloud-fog")
_register_weather_codes([51, 53, 55, 56, 57], "Light drizzle", "cloud-drizzle")
_register_weather_codes([61, 63, 65], "Rain", "cloud-rain")
_register_weather_codes([66, 67], "Icy rain", "cloud-rain")
_register_weather_codes([71, 73, 75, 77], "Snow", "cloud-snow")
_register_weather_codes([80, 81, 82], "Rain showers", "cloud-rain")
_register_weather_codes([85, 86], "Snow showers", "cloud-snow")
_register_weather_codes([95, 96, 99], "Thunderstorm", "cloud-lightning")


def normalize_unit(value: str | None) -> Literal["celsius", "fahrenheit"]:
    """Normalize user-supplied units into the Open-Meteo expected values."""

    if value is None:
        return "fahrenheit"

    normalized = value.strip().lower()
    if normalized in {"c", "cel", "celsius", "metric", "°c"}:
        return "celsius"
    if normalized in {"f", "fahr", "fahrenheit", "imperial", "°f"}:
        return "fahrenheit"
    raise WeatherLookupError("Units must be either 'celsius' or 'fahrenheit'.")


async def retrieve_weather(query: str, unit: str | None = None) -> WeatherWidgetData:
    """Fetch and transform weather data for the provided location."""

    location_query = query.strip()
    _debug("retrieve_weather invoked", extra={"query": location_query, "unit": unit})
    if not location_query:
        raise WeatherLookupError("Please provide a city, address, or landmark to look up.")

    normalized_unit = normalize_unit(unit)

    geocoded: GeocodedLocation | None = None
    forecast: dict[str, Any] | None = None
    try:
        async with httpx.AsyncClient(
            timeout=DEFAULT_TIMEOUT,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
            trust_env=True,
        ) as client:
            geocoded = await _geocode_location(client, location_query)
            _debug(
                "geocode lookup succeeded",
                extra={
                    "label": geocoded.label,
                    "latitude": geocoded.latitude,
                    "longitude": geocoded.longitude,
                },
            )
            _debug("requesting forecast", extra={"unit": normalized_unit})
            forecast = await _fetch_weather_forecast(client, geocoded, normalized_unit)
            forecast_keys = sorted(forecast.keys()) if isinstance(forecast, dict) else "unexpected"
            has_current = bool(forecast.get("current")) if isinstance(forecast, dict) else False
            _debug(
                "forecast received",
                extra={
                    "keys": forecast_keys,
                    "has_current": has_current,
                },
            )
    except httpx.HTTPStatusError as exc:
        _debug(
            "http status error during weather lookup",
            extra={
                "status_code": getattr(exc.response, "status_code", None),
                "query": location_query,
            },
        )
        raise WeatherLookupError("The weather service returned an error response.") from exc
    except httpx.RequestError as exc:
        _debug(
            "request error during weather lookup",
            extra={"error": str(exc), "query": location_query},
        )
        raise WeatherLookupError("Unable to contact the weather service at the moment.") from exc

    if geocoded is None or forecast is None:
        _debug(
            "weather lookup completed without data",
            extra={"geocoded": geocoded, "forecast": forecast is not None},
        )
        raise WeatherLookupError("Weather data is currently unavailable for that location.")

    try:
        _debug(
            "building widget data",
            extra={
                "location": geocoded.label if geocoded else None,
                "unit": normalized_unit,
            },
        )
        widget_data = _build_widget_data(geocoded, forecast, normalized_unit)
    except Exception as exc:  # noqa: BLE001
        _debug(
            "failed to build widget data",
            extra={
                "location": geocoded.label if geocoded else None,
                "error": str(exc),
            },
        )
        raise WeatherLookupError(
            "Weather data is currently unavailable for that location."
        ) from exc
    if widget_data.temperature is None:
        _debug(
            "weather data missing temperature",
            extra={"location": geocoded.label if geocoded else None},
        )
        raise WeatherLookupError("Weather data is currently unavailable for that location.")

    _debug(
        "weather data ready",
        extra={
            "location": widget_data.location,
            "temperature": widget_data.temperature,
            "unit": widget_data.temperature_unit,
        },
    )

    return widget_data


async def _geocode_location(client: httpx.AsyncClient, query: str) -> GeocodedLocation:
    providers = (
        ("nominatim", _geocode_with_nominatim),
        ("open-meteo", _geocode_with_open_meteo),
    )
    last_error: WeatherLookupError | None = None

    for provider_name, provider in providers:
        try:
            location = await provider(client, query)
            return location
        except httpx.HTTPStatusError as exc:
            err = WeatherLookupError("The geocoding service returned an error response.")
            err.__cause__ = exc
            last_error = err
        except httpx.RequestError as exc:
            _debug(
                "geocode provider request error",
                extra={"provider": provider_name, "error": str(exc)},
            )
            err = WeatherLookupError("Unable to contact the geocoding service at the moment.")
            err.__cause__ = exc
            last_error = err
        except WeatherLookupError as exc:
            _debug(
                "geocode provider failed",
                extra={"provider": provider_name, "reason": str(exc)},
            )
            last_error = exc

    if last_error is not None:
        raise last_error

    raise WeatherLookupError("I couldn't find that location. Try another nearby city or landmark.")


async def _geocode_with_nominatim(client: httpx.AsyncClient, query: str) -> GeocodedLocation:
    response = await client.get(
        GEOCODE_URL,
        params={
            "q": query,
            "format": "json",
            "limit": 1,
            "addressdetails": 1,
        },
    )
    response.raise_for_status()
    payload = response.json()
    if not payload:
        raise WeatherLookupError(
            "I couldn't find that location. Try another nearby city or landmark."
        )

    first = payload[0]
    try:
        latitude = float(first["lat"])
        longitude = float(first["lon"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherLookupError(
            "The location data returned from the geocoder was incomplete."
        ) from exc

    label = _format_location_label(first)
    return GeocodedLocation(latitude=latitude, longitude=longitude, label=label, raw=first)


async def _geocode_with_open_meteo(client: httpx.AsyncClient, query: str) -> GeocodedLocation:
    response = await client.get(
        OPEN_METEO_GEOCODE_URL,
        params={"name": query, "count": 1, "language": "en", "format": "json"},
    )
    response.raise_for_status()
    payload = response.json()
    results = payload.get("results") if isinstance(payload, dict) else None
    if not results:
        raise WeatherLookupError(
            "I couldn't find that location. Try another nearby city or landmark."
        )

    first = results[0]
    try:
        latitude = float(first["latitude"])
        longitude = float(first["longitude"])
    except (KeyError, TypeError, ValueError) as exc:
        raise WeatherLookupError(
            "The location data returned from the geocoder was incomplete."
        ) from exc

    label = _format_open_meteo_label(first)
    return GeocodedLocation(latitude=latitude, longitude=longitude, label=label, raw=first)


async def _fetch_weather_forecast(
    client: httpx.AsyncClient,
    location: GeocodedLocation,
    unit: Literal["celsius", "fahrenheit"],
) -> dict[str, Any]:
    params: dict[str, str | int | float | bool | None] = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": CURRENT_FIELDS,
        "hourly": HOURLY_FIELDS,
        "daily": DAILY_FIELDS,
        "temperature_unit": unit,
        "windspeed_unit": "mph" if unit == "fahrenheit" else "kmh",
        "timezone": "auto",
    }

    response = await client.get(WEATHER_URL, params=params)
    response.raise_for_status()
    return response.json()


def _build_widget_data(
    location: GeocodedLocation,
    forecast: dict[str, Any],
    unit: Literal["celsius", "fahrenheit"],
) -> WeatherWidgetData:
    tz = _resolve_timezone(forecast.get("timezone"))
    tz_abbreviation = forecast.get("timezone_abbreviation") or _infer_timezone_abbreviation(tz)

    current = forecast.get("current") or {}
    current_units = forecast.get("current_units") or {}
    daily = forecast.get("daily") or {}
    hourly = forecast.get("hourly") or {}
    hourly_units = forecast.get("hourly_units") or {}

    observation_time = _parse_time(current.get("time"), tz)
    temperature = _to_float(current.get("temperature_2m"))
    feels_like = _to_float(current.get("apparent_temperature"))
    humidity = _to_float(current.get("relative_humidity_2m"))
    wind_speed = _to_float(current.get("wind_speed_10m"))
    wind_direction = _to_float(current.get("wind_direction_10m"))

    weather_code = current.get("weather_code")
    condition, icon = _weather_code_info(weather_code)

    daily_high = _to_float(_first_value(daily.get("temperature_2m_max")))
    daily_low = _to_float(_first_value(daily.get("temperature_2m_min")))
    precipitation = _to_float(_first_value(daily.get("precipitation_probability_max")))
    sunrise = _parse_time(_first_value(daily.get("sunrise")), tz)
    sunset = _parse_time(_first_value(daily.get("sunset")), tz)

    hourly_forecasts = _build_hourly_forecasts(
        hourly,
        hourly_units,
        tz,
        observation_time,
    )

    temperature_unit = current_units.get("temperature_2m") or (
        "°F" if unit == "fahrenheit" else "°C"
    )

    return WeatherWidgetData(
        location=location.label,
        observation_time=observation_time,
        timezone_abbreviation=tz_abbreviation or "",
        temperature=temperature,
        temperature_unit=temperature_unit,
        condition=condition,
        condition_icon=icon,
        feels_like=feels_like,
        high=daily_high,
        low=daily_low,
        wind_speed=wind_speed,
        wind_direction=wind_direction,
        wind_unit=current_units.get("wind_speed_10m")
        or ("mph" if unit == "fahrenheit" else "km/h"),
        humidity=humidity,
        humidity_unit=current_units.get("relative_humidity_2m") or "%",
        precipitation_probability=precipitation,
        sunrise=sunrise,
        sunset=sunset,
        hourly=tuple(hourly_forecasts),
    )


def _build_hourly_forecasts(
    hourly: dict[str, Any],
    hourly_units: dict[str, Any],
    tz: ZoneInfo | None,
    observation_time: datetime | None,
) -> list[HourlyForecast]:
    times = hourly.get("time") or []
    temperatures = hourly.get("temperature_2m") or []
    codes = hourly.get("weather_code") or []
    unit = hourly_units.get("temperature_2m") or "°"

    forecasts: list[HourlyForecast] = []
    for time_str, temp, code in zip(times, temperatures, codes):
        moment = _parse_time(time_str, tz)
        if observation_time and moment and moment < observation_time:
            continue
        condition, icon = _weather_code_info(code)
        forecasts.append(
            HourlyForecast(
                time=moment,
                temperature=_to_float(temp),
                temperature_unit=unit,
                condition=condition,
                icon=icon,
            )
        )
        if len(forecasts) >= HOURLY_SEGMENTS:
            break
    return forecasts


def _weather_code_info(code: Any) -> tuple[str, str]:
    try:
        numeric = int(code)
    except (TypeError, ValueError):
        condition, icon_key = "Current conditions", DEFAULT_ICON_KEY
    else:
        condition, icon_key = WEATHER_CODE_LOOKUP.get(
            numeric, ("Current conditions", DEFAULT_ICON_KEY)
        )

    return condition, icon_key


def _resolve_timezone(name: str | None) -> ZoneInfo | None:
    if not name:
        return None
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        return None


def _infer_timezone_abbreviation(tz: ZoneInfo | None) -> str:
    if tz is None:
        return ""
    now = datetime.now(tz)
    return now.tzname() or ""


def _parse_time(value: Any, tz: ZoneInfo | None) -> datetime | None:
    if not value:
        return None
    try:
        text = str(value)
        if text.endswith("Z"):
            text = text.replace("Z", "+00:00")
        moment = datetime.fromisoformat(text)
    except (TypeError, ValueError):
        return None

    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    if tz is not None:
        moment = moment.astimezone(tz)
    return moment


def _to_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _first_value(values: Any) -> Any:
    if isinstance(values, (list, tuple)) and values:
        return values[0]
    return None


def _format_location_label(result: dict[str, Any]) -> str:
    address = result.get("address") or {}
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("hamlet")
        or address.get("municipality")
        or address.get("county")
    )
    region = address.get("state") or address.get("province") or address.get("state_district")
    country = address.get("country")

    parts = [part for part in (city, region, country) if part]
    if parts:
        if len(parts) > 2:
            return ", ".join(parts[:2])
        return ", ".join(parts)

    display = result.get("display_name")
    if isinstance(display, str) and display:
        pieces = [segment.strip() for segment in display.split(",") if segment.strip()]
        if pieces:
            return ", ".join(pieces[:2])

    return "Selected location"


def _format_open_meteo_label(result: dict[str, Any]) -> str:
    name = result.get("name")
    admin1 = result.get("admin1") or result.get("admin2")
    country = result.get("country")

    parts = [part for part in (name, admin1, country) if part]
    if parts:
        if len(parts) > 2:
            return ", ".join(parts[:2])
        return ", ".join(parts)

    return "Selected location"
