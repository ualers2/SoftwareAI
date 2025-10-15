from typing_extensions import TypedDict, Any
from agents import Agent, ModelSettings, function_tool, FileSearchTool, WebSearchTool, Runner
from datetime import datetime
import pytz

class GetTimeOptions(TypedDict, total=False):
    timezone: str  # Ex: "America/Sao_Paulo", "UTC", etc.
    format: str    # Ex: "%Y-%m-%d %H:%M:%S" ou "iso"

@function_tool
def autogetcurrenttime(options: GetTimeOptions = None) -> dict[str, Any]:
    """
    Retorna o horário atual com base no timezone e formato especificados.

    Parameters
    ----------
    options : dict (opcional)
        {
          "timezone": "America/Sao_Paulo",  # timezone válido do pytz
          "format": "%Y-%m-%d %H:%M:%S"     # ou "iso" para formato ISO 8601
        }

    Returns
    -------
    dict:
        {
          "status": "success",
          "datetime": "2025-10-07 12:34:56",
          "timezone": "America/Sao_Paulo"
        }
    """
    try:
        # Valores padrão
        if options is None:
            options = {}

        tz_name = options.get("timezone", "America/Sao_Paulo")
        fmt = options.get("format", "%Y-%m-%d %H:%M:%S")

        # Configurar timezone
        try:
            tz = pytz.timezone(tz_name)
        except Exception:
            tz = pytz.timezone("UTC")
            tz_name = "UTC"

        now = datetime.now(tz)

        # Formatar saída
        if fmt.lower() == "iso":
            now_str = now.isoformat()
        else:
            now_str = now.strftime(fmt)

        return {
            "status": "success",
            "datetime": now_str,
            "timezone": tz_name
        }

    except Exception as e:
        print(f"💥 Erro em autogetcurrenttime: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
