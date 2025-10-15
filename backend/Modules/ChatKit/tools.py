
import logging
import os
import json
import asyncio
from datetime import datetime
from pydantic import BaseModel
from typing import Annotated, Any, AsyncIterator, Final, Literal, List,TypedDict, AsyncGenerator
from agents import Agent, RunContextWrapper, Runner, function_tool
from chatkit.agents import (
    AgentContext,
    ClientToolCall,
    ThreadItemConverter,
    stream_agent_response, 
    accumulate_text
)
from chatkit.widgets import *

from .facts import Fact, fact_store
from .sample_widget import render_weather_widget, weather_widget_copy_text
from .weather import (
    WeatherLookupError,
    retrieve_weather,
)
from .weather import (
    normalize_unit as normalize_temperature_unit,
)
from .FactAgentContext import FactAgentContext
from .utils import (_stream_saved_hidden,
                    _normalize_color_scheme, 
                    CLIENT_THEME_TOOL_NAME,
                    
                    )

from .data_tools.data import *


diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
os.makedirs(os.path.join(diretorio_script, '../',  '../', 'Logs'), exist_ok=True)
file_handler = logging.FileHandler(os.path.join(diretorio_script,  '../',  '../', 'Logs', 'tools.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)



@function_tool(description_override="Record a fact shared by the user so it is saved immediately.")
async def save_fact(
    ctx: RunContextWrapper[FactAgentContext],
    fact: str,
) -> dict[str, str] | None:
    try:
        saved = await fact_store.create(text=fact)
        confirmed = await fact_store.mark_saved(saved.id)
        if confirmed is None:
            raise ValueError("Failed to save fact")
        await _stream_saved_hidden(ctx, confirmed)
        ctx.context.client_tool_call = ClientToolCall(
            name="record_fact",
            arguments={"fact_id": confirmed.id, "fact_text": confirmed.text},
        )
        print(f"FACT SAVED: {confirmed}")
        return {"fact_id": confirmed.id, "status": "saved"}
    except Exception:
        logging.exception("Failed to save fact")
        return None


@function_tool(
    description_override="Switch the chat interface between light and dark color schemes."
)
async def switch_theme(
    ctx: RunContextWrapper[FactAgentContext],
    theme: str,
) -> dict[str, str] | None:
    logging.debug(f"Switching theme to {theme}")
    try:
        requested = _normalize_color_scheme(theme)
        ctx.context.client_tool_call = ClientToolCall(
            name=CLIENT_THEME_TOOL_NAME,
            arguments={"theme": requested},
        )
        return {"theme": requested}
    except Exception:
        logging.exception("Failed to switch theme")
        return None


@function_tool(
    description_override="Look up the current weather and upcoming forecast for a location and render an interactive weather dashboard."
)
async def get_weather(
    ctx: RunContextWrapper[FactAgentContext],
    location: str,
    unit: Literal["celsius", "fahrenheit"] | str | None = None,
) -> dict[str, str | None]:
    print("[WeatherTool] tool invoked", {"location": location, "unit": unit})
    try:
        normalized_unit = normalize_temperature_unit(unit)
    except WeatherLookupError as exc:
        print("[WeatherTool] invalid unit", {"error": str(exc)})
        raise ValueError(str(exc)) from exc

    try:
        data = await retrieve_weather(location, normalized_unit)
    except WeatherLookupError as exc:
        print("[WeatherTool] lookup failed", {"error": str(exc)})
        raise ValueError(str(exc)) from exc

    print(
        "[WeatherTool] lookup succeeded",
        {
            "location": data.location,
            "temperature": data.temperature,
            "unit": data.temperature_unit,
        },
    )
    try:
        widget = render_weather_widget(data)
        copy_text = weather_widget_copy_text(data)
        payload: Any
        try:
            payload = widget.model_dump()
        except AttributeError:
            payload = widget
        print("[WeatherTool] widget payload", payload)
    except Exception as exc:  # noqa: BLE001
        print("[WeatherTool] widget build failed", {"error": str(exc)})
        raise ValueError("Weather data is currently unavailable for that location.") from exc

    print("[WeatherTool] streaming widget")
    try:
        await ctx.context.stream_widget(widget, copy_text=copy_text)
    except Exception as exc:  # noqa: BLE001
        print("[WeatherTool] widget stream failed", {"error": str(exc)})
        raise ValueError("Weather data is currently unavailable for that location.") from exc

    print("[WeatherTool] widget streamed")

    observed = data.observation_time.isoformat() if data.observation_time else None

    return {
        "location": data.location,
        "unit": normalized_unit,
        "observed_at": observed,
    }

@function_tool(
    description_override="Retorna o número de tarefas ou operações concluídas por um agente (ex: 'pr_ai_ci', 'gcl_electron') em um período. Use para responder perguntas sobre produtividade ou status de execução."
)
async def get_agent_activity_count(
    ctx: RunContextWrapper[FactAgentContext],
    agent_name: str,
    time_range: Literal["daily", "weekly", "monthly", "total"] | str,
) -> str:
    """
    Simula a consulta ao banco de dados para obter a contagem de atividades do agente.
    Na implementação real, você usaria o `ctx.context.request_context` para obter o
    ID do usuário ou credenciais e executaria uma consulta ao seu sistema de logs.
    """
    
    # Simulação de dados de resposta para diferentes agentes e períodos.
    # O LLM receberá esta string e a usará para formular a resposta final.
    logger.info("get_agent_activity_count called")
    agent_name = agent_name.lower().strip()
    time_range = time_range.lower().strip()

    if agent_name == "pr_ai_ci":
        if time_range == "daily":
            return "O agente PR AI concluiu 12 execuções de Pull Request nas últimas 24 horas. 95% dessas execuções resultaram em aprovação automática da mensagem de commit."
        if time_range == "weekly":
            return "O agente PR AI concluiu 78 execuções nesta semana, gerando uma economia de 4 horas no tempo de revisão manual das mensagens."
        if time_range == "monthly":
            return "O agente PR AI processou 310 Pull Requests neste mês."
        if time_range == "total":
            return "O agente PR AI já processou 4.582 Pull Requests desde o lançamento do PR AI."
    
    if agent_name == "gcl_electron":
        if time_range == "daily":
            return "O Git Context Layer (GCL) processou 41 commits na camada de pré-staging hoje, com uma taxa de precisão de 98% na sugestão de mensagens de commit."
        if time_range == "weekly":
            return "O GCL foi invocado 215 vezes na última semana."

    return f"Não foram encontrados dados de atividade para o agente '{agent_name}' no período '{time_range}'. Certifique-se de que o nome do agente é válido (ex: pr_ai_ci ou gcl_electron)."


@function_tool(
    description_override="Recupera o valor atual de uma configuração de limite (threshold) do GCL (Git Context Layer). Use para responder perguntas sobre os limites operacionais de linhas ou arquivos."
)
async def get_gcl_threshold_config(
    ctx: RunContextWrapper[FactAgentContext],
    setting_key: Annotated[
        str,
        "A chave da configuração do limite que o usuário está perguntando. Deve ser 'lines_threshold' para limite de linhas ou 'files_threshold' para limite de arquivos.",
    ],
) -> str:
    """
    Simula a recuperação de uma configuração de threshold do GCL.
    """
    logger.info(f"get_gcl_threshold_config called for key: {setting_key}")
    key = setting_key.lower().strip()

    if key == "lines_threshold":
        # Limite atual simulado: 500 linhas de mudança
        return "O limite máximo de linhas para a análise do GCL (lines_threshold) está configurado como 500. Commits que excedem este valor são ignorados ou sinalizados para revisão manual."
    
    if key == "files_threshold":
        # Limite atual simulado: 10 arquivos
        return "O limite máximo de arquivos (files_threshold) para uma única execução do GCL é de 10. Commits que modificam mais do que 10 arquivos não disparam o processo de sugestão automática."

    return f"A chave de configuração '{setting_key}' não é reconhecida. As chaves válidas são 'lines_threshold' e 'files_threshold'."


@function_tool(description_override="Display a dynamic chart widget to the user.")
async def chart_generator(ctx: RunContextWrapper[AgentContext], data: ChartData) -> None:
    """
    Gera um gráfico dinâmico e customizável com base nos dados e configurações fornecidas.
    """
    logger = logging.getLogger(__name__)
    logger.info("Iniciando chart_generator com dados do modelo ChartData.")

    async def widget_generator() -> AsyncGenerator:
        # Cria as séries dinamicamente com base no modelo recebido
        chart_series = []
        for s in data.series:
            if s.type == "bar":
                chart_series.append(BarSeries(dataKey=s.dataKey, label=s.label))
            elif s.type == "line":
                chart_series.append(LineSeries(dataKey=s.dataKey, label=s.label))
            else:
                logger.warning(f"Tipo de série desconhecido: {s.type}")

        # Estado inicial (gráfico vazio)
        yield Card(
            children=[
                Title(value=data.title, size="xl"),
                Chart(id=data.id, data=[], series=chart_series, xAxis=data.xAxis),
            ]
        )

        progressive_data = []
        for i, point in enumerate(data.points):
            progressive_data.append(point.dict())
            logger.debug(f"Atualizando gráfico com novo ponto: {point.dict()}")

            await asyncio.sleep(0.8)  # streaming gradual (remova se quiser render imediato)

            yield Card(
                children=[
                    Title(value=data.title, size="xl"),
                    Chart(
                        id=data.id,
                        data=progressive_data,
                        series=chart_series,
                        xAxis=data.xAxis,
                        showLegend=True,
                        showTooltip=True,
                        height=260,
                    ),
                ]
            )

        logger.info("Finalizando chart_generator com sucesso.")

    await ctx.context.stream_widget(widget_generator())


@function_tool(description_override="Display a sample widget to the user.")
async def sample_widget(ctx: RunContextWrapper[AgentContext]) -> None:
    short_title = Agent(
        model="gpt-4.1-mini",
        name="short title conversation",
        instructions="voce tem uma responsabilidade, crie titulos curtos para as conversas",
    )

    description_text = Runner.run_streamed(
        short_title, "ChatKit is the best thing ever"
    )
    async def widget_generator() -> AsyncGenerator[WidgetComponent, None]:
        text_widget_updates = accumulate_text(
            description_text.stream_events(),
            Text(
                id="description",
                value="",
                streaming=True
            ),
        )

        async for text_widget in text_widget_updates:
            yield Card(
                children=[text_widget]
            )

    await ctx.context.stream_widget(widget_generator())


















