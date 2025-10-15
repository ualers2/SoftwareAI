from __future__ import annotations

import base64
from dataclasses import dataclass, field
from datetime import datetime
from typing import Sequence

from chatkit.widgets import (
    Box,
    Card,
    Col,
    Image,
    Row,
    Text,
    Title,
    WidgetComponent,
    WidgetRoot,
)

WEATHER_ICON_COLOR = "#1D4ED8"
WEATHER_ICON_ACCENT = "#DBEAFE"


def _sun_svg() -> str:
    color = WEATHER_ICON_COLOR
    accent = WEATHER_ICON_ACCENT
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        f'<circle cx="32" cy="32" r="13" fill="{accent}" stroke="{color}" stroke-width="3"/>'
        f'<g stroke="{color}" stroke-width="3" stroke-linecap="round">'
        '<line x1="32" y1="8" x2="32" y2="16"/>'
        '<line x1="32" y1="48" x2="32" y2="56"/>'
        '<line x1="8" y1="32" x2="16" y2="32"/>'
        '<line x1="48" y1="32" x2="56" y2="32"/>'
        '<line x1="14.93" y1="14.93" x2="20.55" y2="20.55"/>'
        '<line x1="43.45" y1="43.45" x2="49.07" y2="49.07"/>'
        '<line x1="14.93" y1="49.07" x2="20.55" y2="43.45"/>'
        '<line x1="43.45" y1="20.55" x2="49.07" y2="14.93"/>'
        "</g>"
        "</svg>"
    )


def _sun_peek_svg() -> str:
    color = WEATHER_ICON_COLOR
    accent = WEATHER_ICON_ACCENT
    return (
        f"<g>"
        f'<circle cx="20" cy="22" r="9" fill="{accent}" stroke="{color}" stroke-width="3"/>'
        f'<g stroke="{color}" stroke-width="3" stroke-linecap="round">'
        '<line x1="20" y1="10" x2="20" y2="14"/>'
        '<line x1="20" y1="30" x2="20" y2="34"/>'
        '<line x1="8" y1="22" x2="12" y2="22"/>'
        '<line x1="28" y1="22" x2="32" y2="22"/>'
        '<line x1="12" y1="14" x2="14" y2="16"/>'
        '<line x1="26" y1="28" x2="28" y2="30"/>'
        '<line x1="12" y1="30" x2="14" y2="28"/>'
        '<line x1="26" y1="16" x2="28" y2="14"/>'
        "</g>"
        "</g>"
    )


def _fog_lines_svg() -> str:
    color = WEATHER_ICON_COLOR
    return (
        f'<g stroke="{color}" stroke-width="3" stroke-linecap="round">'
        '<line x1="18" y1="50" x2="42" y2="50"/>'
        '<line x1="24" y1="56" x2="48" y2="56"/>'
        "</g>"
    )


def _drizzle_lines_svg() -> str:
    color = WEATHER_ICON_COLOR
    return (
        f'<g stroke="{color}" stroke-width="3" stroke-linecap="round">'
        '<line x1="26" y1="50" x2="26" y2="56"/>'
        '<line x1="36" y1="52" x2="36" y2="58"/>'
        '<line x1="46" y1="50" x2="46" y2="56"/>'
        "</g>"
    )


def _rain_lines_svg() -> str:
    color = WEATHER_ICON_COLOR
    return (
        f'<g stroke="{color}" stroke-width="3" stroke-linecap="round">'
        '<line x1="26" y1="48" x2="30" y2="56"/>'
        '<line x1="36" y1="50" x2="40" y2="58"/>'
        '<line x1="46" y1="48" x2="50" y2="56"/>'
        "</g>"
    )


def _snow_symbols_svg() -> str:
    color = WEATHER_ICON_COLOR
    return (
        f'<g stroke="{color}" stroke-width="2" stroke-linecap="round">'
        '<line x1="24" y1="50" x2="24" y2="58"/>'
        '<line x1="21" y1="53" x2="27" y2="55"/>'
        '<line x1="21" y1="55" x2="27" y2="53"/>'
        '<line x1="40" y1="50" x2="40" y2="58"/>'
        '<line x1="37" y1="53" x2="43" y2="55"/>'
        '<line x1="37" y1="55" x2="43" y2="53"/>'
        "</g>"
    )


def _lightning_svg() -> str:
    color = WEATHER_ICON_COLOR
    return (
        f'<path d="M34 46L28 56H34L30 64L42 50H36L40 46Z" '
        f'fill="{color}" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>'
    )


def _cloud_svg(before: str = "", after: str = "") -> str:
    color = WEATHER_ICON_COLOR
    accent = WEATHER_ICON_ACCENT
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        f"{before}"
        f'<path d="M22 46H44C50.075 46 55 41.075 55 35S50.075 24 44 24H42.7C41.2 16.2 34.7 10 26.5 10 18 10 11.6 16.1 11 24.3 6.5 25.6 3 29.8 3 35s4.925 11 11 11h8Z" '
        f'fill="{accent}" stroke="{color}" stroke-width="3" stroke-linejoin="round"/>'
        f"{after}"
        "</svg>"
    )


WEATHER_ICON_SVGS: dict[str, str] = {
    "sun": _sun_svg(),
    "cloud": _cloud_svg(),
    "cloud-sun": _cloud_svg(before=_sun_peek_svg()),
    "cloud-fog": _cloud_svg(after=_fog_lines_svg()),
    "cloud-drizzle": _cloud_svg(after=_drizzle_lines_svg()),
    "cloud-rain": _cloud_svg(after=_rain_lines_svg()),
    "cloud-snow": _cloud_svg(after=_snow_symbols_svg()),
    "cloud-lightning": _cloud_svg(after=_lightning_svg()),
}


def _encode_svg(svg: str) -> str:
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


WEATHER_ICON_SOURCES: dict[str, str] = {
    name: _encode_svg(svg) for name, svg in WEATHER_ICON_SVGS.items()
}


DEFAULT_WEATHER_ICON_SRC = WEATHER_ICON_SOURCES["cloud"]


def _weather_icon_src(name: str | None) -> str:
    if not name:
        return DEFAULT_WEATHER_ICON_SRC
    return WEATHER_ICON_SOURCES.get(name, DEFAULT_WEATHER_ICON_SRC)


def _wind_detail_svg() -> str:
    color = WEATHER_ICON_COLOR
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        f'<path d="M12 22h26c4.418 0 8-3.582 8-8" stroke="{color}" stroke-width="4" '
        'stroke-linecap="round"/>'
        f'<path d="M18 32h30c5.523 0 10-4.477 10-10" stroke="{color}" stroke-width="4" '
        'stroke-linecap="round"/>'
        f'<path d="M18 42h22c3.314 0 6 2.686 6 6" stroke="{color}" stroke-width="4" '
        'stroke-linecap="round"/>'
        "</svg>"
    )


def _humidity_detail_svg() -> str:
    color = WEATHER_ICON_COLOR
    accent = WEATHER_ICON_ACCENT
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        f'<path d="M32 8c10 10 18 20 18 30a18 18 0 1 1-36 0c0-10 8-20 18-30Z" '
        f'fill="{accent}" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="M32 36c3.314 0 6 2.686 6 6s-2.686 6-6 6" stroke="{color}" '
        'stroke-width="4" stroke-linecap="round"/>'
        "</svg>"
    )


def _precipitation_detail_svg() -> str:
    color = WEATHER_ICON_COLOR
    accent = WEATHER_ICON_ACCENT
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        f'<path d="M18 30c0-8.837 7.163-16 16-16 7.732 0 14 5.318 15.678 12.362" '
        f'stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M46 26c6.075 0 11 4.925 11 11s-4.925 11-11 11H20c-6.075 0-11-4.925-11-11 0-5.302 3.734-9.711 8.693-10.793" '
        f'fill="{accent}" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'
        f'<path d="M24 50l-4 8" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M34 50l-4 8" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M44 50l-4 8" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        "</svg>"
    )


def _sunrise_detail_svg(rising: bool) -> str:
    color = WEATHER_ICON_COLOR
    accent = WEATHER_ICON_ACCENT
    sun_y = "30" if rising else "34"
    rays_top = (
        '<line x1="32" y1="10" x2="32" y2="6"/>'
        if rising
        else '<line x1="32" y1="44" x2="32" y2="48"/>'
    )
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        f'<path d="M14 44h36" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        f'<path d="M12 54h40" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        f'<circle cx="32" cy="{sun_y}" r="10" fill="{accent}" stroke="{color}" stroke-width="4"/>'
        f'<g stroke="{color}" stroke-width="4" stroke-linecap="round">'
        f"{rays_top}"
        '<line x1="16" y1="30" x2="12" y2="26"/>'
        '<line x1="48" y1="30" x2="52" y2="26"/>'
        "</g>"
        "</svg>"
    )


def _thermometer_detail_svg() -> str:
    color = WEATHER_ICON_COLOR
    accent = WEATHER_ICON_ACCENT
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">'
        f'<path d="M30 12a6 6 0 0 1 12 0v28.343a12 12 0 1 1-12 0V12Z" '
        f'fill="{accent}" stroke="{color}" stroke-width="4" stroke-linejoin="round"/>'
        f'<circle cx="36" cy="46" r="6" fill="{color}"/>'
        f'<path d="M36 24v14" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
        "</svg>"
    )


DETAIL_ICON_SVGS: dict[str, str] = {
    "wind": _wind_detail_svg(),
    "humidity": _humidity_detail_svg(),
    "precipitation": _precipitation_detail_svg(),
    "sunrise": _sunrise_detail_svg(rising=True),
    "sunset": _sunrise_detail_svg(rising=False),
    "thermometer": _thermometer_detail_svg(),
}


DETAIL_ICON_SOURCES: dict[str, str] = {
    name: _encode_svg(svg) for name, svg in DETAIL_ICON_SVGS.items()
}


DEFAULT_DETAIL_ICON_KEY = "thermometer"


DETAIL_ICON_MAP: dict[str, str] = {
    "wind": "wind",
    "droplets": "humidity",
    "umbrella": "precipitation",
    "sunrise": "sunrise",
    "sunset": "sunset",
    "feels_like": "thermometer",
}


def _detail_icon_src(name: str) -> str:
    key = DETAIL_ICON_MAP.get(name, DEFAULT_DETAIL_ICON_KEY)
    return DETAIL_ICON_SOURCES.get(key, DETAIL_ICON_SOURCES[DEFAULT_DETAIL_ICON_KEY])


@dataclass(frozen=True)
class HourlyForecast:
    """Represents a single entry in the short term forecast."""

    time: datetime | None
    temperature: float | None
    temperature_unit: str
    condition: str
    icon: str


@dataclass(frozen=True)
class WeatherWidgetData:
    """Container for the information rendered by the weather widget."""

    location: str
    observation_time: datetime | None
    timezone_abbreviation: str
    temperature: float | None
    temperature_unit: str
    condition: str
    condition_icon: str
    feels_like: float | None = None
    high: float | None = None
    low: float | None = None
    wind_speed: float | None = None
    wind_direction: float | None = None
    wind_unit: str | None = None
    humidity: float | None = None
    humidity_unit: str | None = None
    precipitation_probability: float | None = None
    sunrise: datetime | None = None
    sunset: datetime | None = None
    hourly: Sequence[HourlyForecast] = field(default_factory=tuple)


def render_weather_widget(data: WeatherWidgetData) -> WidgetRoot:
    """Build a modern weather dashboard widget from processed weather data."""

    temperature_text = _format_temperature(data.temperature, data.temperature_unit)
    high_low_text = _format_high_low(data.high, data.low, data.temperature_unit)
    updated_text = _format_updated_label(data.observation_time, data.timezone_abbreviation)

    header = Box(
        padding=5,
        background="surface-tertiary",
        children=[
            Col(
                gap=4,
                children=_compact(
                    [
                        Row(
                            justify="between",
                            align="center",
                            children=_compact(
                                [
                                    Col(
                                        align="start",
                                        gap=1,
                                        children=_compact(
                                            [
                                                Text(
                                                    value=data.location,
                                                    size="lg",
                                                    weight="semibold",
                                                ),
                                                Text(
                                                    value=updated_text,
                                                    color="tertiary",
                                                    size="xs",
                                                )
                                                if updated_text
                                                else None,
                                            ]
                                        ),
                                    ),
                                    Box(
                                        padding=3,
                                        radius="full",
                                        background="blue-100",
                                        children=[
                                            Image(
                                                src=_weather_icon_src(data.condition_icon),
                                                alt=data.condition or "Current conditions",
                                                size=28,
                                                fit="contain",
                                            )
                                        ],
                                    ),
                                ]
                            ),
                        ),
                        Row(
                            align="start",
                            gap=4,
                            children=_compact(
                                [
                                    Title(
                                        value=temperature_text,
                                        size="lg",
                                        weight="semibold",
                                    ),
                                    Col(
                                        align="start",
                                        gap=1,
                                        children=_compact(
                                            [
                                                Text(
                                                    value=data.condition,
                                                    color="secondary",
                                                    size="sm",
                                                    weight="medium",
                                                ),
                                                Text(
                                                    value=high_low_text,
                                                    color="tertiary",
                                                    size="xs",
                                                )
                                                if high_low_text
                                                else None,
                                            ]
                                        ),
                                    ),
                                ]
                            ),
                        ),
                    ]
                ),
            ),
        ],
    )

    details_section = _build_details_section(data)
    hourly_section = _build_hourly_section(data)

    body_children: list[WidgetComponent] = []
    if details_section is not None:
        body_children.append(details_section)
    if hourly_section is not None:
        body_children.append(hourly_section)

    body = Box(padding=5, gap=4, children=body_children)

    return Card(
        key="weather",
        padding=0,
        children=_compact([header, body if body_children else None]),
    )


def weather_widget_copy_text(data: WeatherWidgetData) -> str:
    """Generate human-readable fallback text for the weather widget."""

    segments: list[str] = []

    time_text = _format_updated_label(data.observation_time, data.timezone_abbreviation, short=True)
    temperature_text = _format_temperature(data.temperature, data.temperature_unit)
    condition_text = data.condition.lower() if data.condition else "unknown conditions"
    location_text = data.location or "the selected location"

    if time_text:
        segments.append(
            f"As of {time_text}, {location_text} is {temperature_text} with {condition_text}."
        )
    else:
        segments.append(
            f"Current weather in {location_text} is {temperature_text} with {condition_text}."
        )

    high_low_text = _format_high_low(data.high, data.low, data.temperature_unit)
    if high_low_text:
        segments.append(high_low_text + ".")

    feels_like_text = _format_feels_like(data.feels_like, data.temperature_unit)
    if feels_like_text:
        segments.append(f"Feels like {feels_like_text}.")

    wind_text = _format_wind(data.wind_speed, data.wind_unit, data.wind_direction)
    if wind_text:
        segments.append(f"Winds {wind_text}.")

    humidity_text = _format_percentage(data.humidity, data.humidity_unit)
    if humidity_text:
        segments.append(f"Humidity {humidity_text}.")

    precipitation_text = _format_probability(data.precipitation_probability)
    if precipitation_text:
        segments.append(f"Precipitation chance {precipitation_text}.")

    sunrise_text = _format_time_of_day(data.sunrise, data.timezone_abbreviation)
    sunset_text = _format_time_of_day(data.sunset, data.timezone_abbreviation)
    if sunrise_text and sunset_text:
        segments.append(f"Sunrise at {sunrise_text} and sunset at {sunset_text}.")
    elif sunrise_text:
        segments.append(f"Sunrise at {sunrise_text}.")
    elif sunset_text:
        segments.append(f"Sunset at {sunset_text}.")

    if data.hourly:
        upcoming: list[str] = []
        for forecast in list(data.hourly)[:4]:
            hour_label = _format_hour_label(forecast.time, data.timezone_abbreviation)
            temp_label = _format_temperature(
                forecast.temperature, forecast.temperature_unit or data.temperature_unit
            )
            condition_label = forecast.condition.lower()
            upcoming.append(f"{hour_label}: {temp_label} {condition_label}")
        if upcoming:
            segments.append("Next hours " + ", ".join(upcoming) + ".")

    return " ".join(segment.strip() for segment in segments if segment).strip()


def _horizontal_scroller(items: Sequence[WidgetComponent]) -> WidgetComponent:
    return Box(
        direction="row",
        wrap="nowrap",
        gap=3,
        width="100%",
        justify="start",
        align="stretch",
        children=list(items),
    )


def _build_details_section(data: WeatherWidgetData) -> WidgetComponent | None:
    wind_text = _format_wind(data.wind_speed, data.wind_unit, data.wind_direction)
    humidity_text = _format_percentage(data.humidity, data.humidity_unit)
    precipitation_text = _format_probability(data.precipitation_probability)
    sunrise_text = _format_time_of_day(data.sunrise, data.timezone_abbreviation)
    sunset_text = _format_time_of_day(data.sunset, data.timezone_abbreviation)
    feels_like_text = _format_feels_like(data.feels_like, data.temperature_unit)

    chips = _compact(
        [
            _detail_chip("Feels like", feels_like_text, "feels_like") if feels_like_text else None,
            _detail_chip("Wind", wind_text, "wind") if wind_text else None,
            _detail_chip("Humidity", humidity_text, "droplets") if humidity_text else None,
            _detail_chip("Precipitation", precipitation_text, "umbrella")
            if precipitation_text
            else None,
            _detail_chip("Sunrise", sunrise_text, "sunrise") if sunrise_text else None,
            _detail_chip("Sunset", sunset_text, "sunset") if sunset_text else None,
        ]
    )

    if not chips:
        return None

    return Col(
        gap=3,
        children=[
            Text(value="Today's highlights", weight="semibold", size="sm"),
            _horizontal_scroller(chips),
        ],
    )


def _build_hourly_section(data: WeatherWidgetData) -> WidgetComponent | None:
    if not data.hourly:
        return None

    cards = [
        _hourly_chip(forecast, data.temperature_unit, data.timezone_abbreviation)
        for forecast in data.hourly
    ]

    if not cards:
        return None

    return Col(
        gap=3,
        children=[
            Text(value="Next hours", weight="semibold", size="sm"),
            _horizontal_scroller(cards),
        ],
    )


def _detail_chip(label: str, value: str, icon: str) -> WidgetComponent:
    return Box(
        padding=3,
        radius="xl",
        background="surface-tertiary",
        width=150,
        minWidth=150,
        maxWidth=150,
        minHeight=100,
        maxHeight=100,
        flex="0 0 auto",
        children=[
            Col(
                align="stretch",
                gap=2,
                children=[
                    Row(
                        gap=2,
                        align="center",
                        children=[
                            Image(src=_detail_icon_src(icon), alt=label, size=28, fit="contain"),
                            Text(value=label, size="xs", weight="medium", color="tertiary"),
                        ],
                    ),
                    Row(
                        justify="center",
                        margin={"top": 4},
                        children=[Text(value=value, weight="semibold", size="lg")],
                    ),
                ],
            )
        ],
    )


def _hourly_chip(
    forecast: HourlyForecast, default_unit: str, timezone_abbreviation: str
) -> WidgetComponent:
    time_label = _format_hour_label(forecast.time, timezone_abbreviation)
    temperature_label = _format_temperature(
        forecast.temperature, forecast.temperature_unit or default_unit
    )

    return Box(
        padding=3,
        radius="xl",
        background="surface-tertiary",
        width=100,
        minWidth=100,
        maxWidth=100,
        minHeight=150,
        maxHeight=150,
        flex="0 0 auto",
        children=[
            Col(
                align="center",
                gap=2,
                children=_compact(
                    [
                        Text(value=time_label, size="xs", color="tertiary", weight="medium"),
                        Image(
                            src=_weather_icon_src(forecast.icon),
                            alt=forecast.condition,
                            size=36,
                            fit="contain",
                        ),
                        Text(value=temperature_label, weight="semibold"),
                        Text(value=forecast.condition, size="xs", color="tertiary"),
                    ]
                ),
            ),
        ],
    )


def _format_temperature(value: float | None, unit: str | None) -> str:
    if value is None:
        return "—"
    try:
        number = round(float(value))
    except (TypeError, ValueError):
        return "—"
    suffix = unit or "°"
    return f"{number}{suffix}"


def _format_high_low(high: float | None, low: float | None, unit: str | None) -> str:
    high_text = _format_temperature(high, unit) if high is not None else ""
    low_text = _format_temperature(low, unit) if low is not None else ""
    if high_text and low_text:
        return f"High {high_text} • Low {low_text}"
    if high_text:
        return f"High {high_text}"
    if low_text:
        return f"Low {low_text}"
    return ""


def _format_feels_like(value: float | None, unit: str | None) -> str:
    if value is None:
        return ""
    return _format_temperature(value, unit)


def _format_wind(speed: float | None, unit: str | None, direction: float | None) -> str:
    if speed is None and direction is None:
        return ""

    parts: list[str] = []
    if speed is not None:
        try:
            speed_value = round(float(speed))
        except (TypeError, ValueError):
            speed_value = None
        if speed_value is not None:
            parts.append(f"{speed_value}{f' {unit}' if unit else ''}".strip())

    cardinal = _wind_direction_to_cardinal(direction)
    if cardinal:
        parts.append(cardinal)

    return " ".join(parts).strip()


def _format_percentage(value: float | None, unit: str | None) -> str:
    if value is None:
        return ""
    try:
        number = round(float(value))
    except (TypeError, ValueError):
        return ""
    suffix = unit or "%"
    return f"{number}{suffix}"


def _format_probability(value: float | None) -> str:
    if value is None:
        return ""
    try:
        number = round(float(value))
    except (TypeError, ValueError):
        return ""
    return f"{number}%"


def _format_time_of_day(moment: datetime | None, tz_abbreviation: str) -> str:
    if moment is None:
        return ""
    time_text = moment.strftime("%I:%M %p").lstrip("0")
    tz = tz_abbreviation.strip()
    return f"{time_text} {tz}".strip()


def _format_hour_label(moment: datetime | None, tz_abbreviation: str) -> str:
    if moment is None:
        return "—"
    hour_text = moment.strftime("%I %p").lstrip("0")
    return hour_text or moment.strftime("%H:%M")


def _format_updated_label(
    moment: datetime | None, tz_abbreviation: str, *, short: bool = False
) -> str:
    if moment is None:
        return ""

    time_text = moment.strftime("%I:%M %p").lstrip("0")
    tz = tz_abbreviation.strip()
    if short:
        return f"{time_text} {tz}".strip()

    date_text = moment.strftime("%b %d").replace(" 0", " ")
    base = f"{date_text} · {time_text}" if date_text else time_text
    return f"Updated {base} {tz}".strip()


def _wind_direction_to_cardinal(direction: float | None) -> str | None:
    if direction is None:
        return None
    try:
        degrees = float(direction)
    except (TypeError, ValueError):
        return None
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = int((degrees + 22.5) // 45) % len(directions)
    return directions[index]


def _compact(items: Sequence[WidgetComponent | None]) -> list[WidgetComponent]:
    return [item for item in items if item is not None]
