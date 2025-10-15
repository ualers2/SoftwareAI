# chat.py
from __future__ import annotations

import os
import asyncio
import inspect
import logging
from datetime import datetime
from typing import Annotated, Any, AsyncIterator, Final, Literal
from uuid import uuid4
from agents import Agent, RunContextWrapper, Runner, ModelSettings,RunConfig, StopAtTools, function_tool, SQLiteSession
from chatkit.server import ChatKitServer, ThreadItemDoneEvent
from chatkit.agents import (
    AgentContext,
    ClientToolCall,
    ThreadItemConverter,
    stream_agent_response,
    stream_widget,
    simple_to_agent_input
)
from chatkit.widgets import (
    Text, Card, Chart, BarSeries, LineSeries, XAxisConfig
)
from chatkit.types import (
    Attachment,
    ClientToolCallItem,
    HiddenContextItem,
    ThreadItem,
    ThreadMetadata,
    ThreadStreamEvent,
    UserMessageItem,
)
from .tools import *
from .utils import (_stream_saved_hidden,
                    _normalize_color_scheme,
                    CLIENT_THEME_TOOL_NAME,
                    _gen_id,
                    _is_tool_completion_item,
                    _thread_item_done,
                    _user_message_text
                    )
from openai.types.responses import ResponseInputContentParam
from .constants import NAME, INSTRUCTIONS, MODEL
from .memory_store import MemoryStore
from .FactAgentContext import FactAgentContext
from chatkit.store import Store
from .postgres_store import PostgresStore
from api import db, app

logging.basicConfig(level=logging.INFO)

class SoftwareAIAgentServer(ChatKitServer[dict[str, Any]]):
    """ChatKit server wired up with the fact-recording tool."""

    def __init__(self, store: Store) -> None: #
        self.store = store
        # self.store: MemoryStore = MemoryStore()
        super().__init__(self.store)
        tools = [
            # save_fact, 
            # switch_theme, 
            # get_weather, 
            get_agent_activity_count,
            get_gcl_threshold_config,
            chart_generator
        ]
        self.assistant = Agent[FactAgentContext](
            model=MODEL,
            name=NAME,
            instructions=INSTRUCTIONS,
            tools=tools, 

        )
        self.short_title = Agent(
            model=MODEL,
            name="short title conversation",
            instructions="voce tem uma responsabilidade, crie titulos curtos para as conversas",
        )
        model_settings = ModelSettings(
            include_usage=True,
            tracing_disabled=True,
            workflow_name="SoftwareAI Chat Kit",
            # parallel_tool_calls=True
        )
        
        self.run_config = RunConfig(
            model_settings=model_settings
        )
        

        os.makedirs(os.path.join(os.path.dirname(__file__), 'Thread_Sessions'), exist_ok=True)
        self._thread_item_converter = self._init_thread_item_converter()

    async def respond(
        self,
        thread: ThreadMetadata,
        item: UserMessageItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        if item is not None:
            asyncio.create_task(self.maybe_update_thread_title(thread, item))

        agent_context = FactAgentContext(
            thread=thread,
            store=self.store,
            request_context=context,
        )

        logging.info(f"inference_options: {item.inference_options}")
        if item.inference_options.tool_choice:
            logging.info(f"inference_options id {item.inference_options.tool_choice.id}")
            model_settings_with_tool = ModelSettings(
                include_usage=True,
                tracing_disabled=True,
                workflow_name="SoftwareAI Chat Kit",
                tool_choice=item.inference_options.tool_choice.id, 
            )
            self.run_config = RunConfig(
                model_settings=model_settings_with_tool
            )
        
        target_item: ThreadItem | None = item
        if target_item is None:
            target_item = await self._latest_thread_item(thread, context)

        if target_item is None or _is_tool_completion_item(target_item):
            return
        

        agent_input = await self._to_agent_input(thread, target_item)
        if agent_input is None:
            return


        session = SQLiteSession(f"{thread.id}", 
                                db_path=os.path.join(os.path.dirname(__file__), 
                                'Thread_Sessions',  
                                f'{thread.id}.db'
                            ))

        result = Runner.run_streamed(
            self.assistant,
            agent_input,
            context=agent_context,
            session=session,
            run_config=self.run_config
        )


        async for event in stream_agent_response(agent_context, result):
            yield event

        # async for event in stream_widget(
        #     thread,
        #     self.chart_generator(),
        #     generate_id=lambda item_type: self.store.generate_item_id(
        #         item_type, thread, context
        #     ),
        # ):
        #     yield event

        return

    async def maybe_update_thread_title(
        self,
        thread: ThreadMetadata,
        input_item: UserMessageItem,
    ) -> None:
        if thread.title is not None:
            return
        agent_input = await simple_to_agent_input(input_item)
        run = await Runner.run(self.short_title, input=agent_input)
        thread.title = run.final_output

    async def to_message_content(self, _input: Attachment) -> ResponseInputContentParam:
        raise RuntimeError("File attachments are not supported in this demo.")

    def _init_thread_item_converter(self) -> Any | None:
        converter_cls = ThreadItemConverter
        if converter_cls is None or not callable(converter_cls):
            return None

        attempts: tuple[dict[str, Any], ...] = (
            {"to_message_content": self.to_message_content},
            {"message_content_converter": self.to_message_content},
            {},
        )

        for kwargs in attempts:
            try:
                return converter_cls(**kwargs)
            except TypeError:
                continue
        return None

    async def _latest_thread_item(
        self, thread: ThreadMetadata, context: dict[str, Any]
    ) -> ThreadItem | None:
        try:
            items = await self.store.load_thread_items(thread.id, None, 999, "desc", context)
            logging.info(f"_latest_thread_item items {items}")
        except Exception:  # pragma: no cover - defensive
            return None

        return items.data[0] if getattr(items, "data", None) else None

    async def _to_agent_input(
        self,
        thread: ThreadMetadata,
        item: ThreadItem,
    ) -> Any | None:
        if _is_tool_completion_item(item):
            return None

        converter = getattr(self, "_thread_item_converter", None)
        if converter is not None:
            for attr in (
                "to_input_item",
                "convert",
                "convert_item",
                "convert_thread_item",
            ):
                method = getattr(converter, attr, None)
                if method is None:
                    continue
                call_args: list[Any] = [item]
                call_kwargs: dict[str, Any] = {}
                try:
                    signature = inspect.signature(method)
                except (TypeError, ValueError):
                    signature = None

                if signature is not None:
                    params = [
                        parameter
                        for parameter in signature.parameters.values()
                        if parameter.kind
                        not in (
                            inspect.Parameter.VAR_POSITIONAL,
                            inspect.Parameter.VAR_KEYWORD,
                        )
                    ]
                    if len(params) >= 2:
                        next_param = params[1]
                        if next_param.kind in (
                            inspect.Parameter.POSITIONAL_ONLY,
                            inspect.Parameter.POSITIONAL_OR_KEYWORD,
                        ):
                            call_args.append(thread)
                        else:
                            call_kwargs[next_param.name] = thread

                result = method(*call_args, **call_kwargs)
                if inspect.isawaitable(result):
                    return await result
                return result

        if isinstance(item, UserMessageItem):
            return _user_message_text(item)

        return None

    async def _add_hidden_item(
        self,
        thread: ThreadMetadata,
        context: dict[str, Any],
        content: str,
    ) -> None:
        await self.store.add_thread_item(
            thread.id,
            HiddenContextItem(
                id=_gen_id("msg"),
                thread_id=thread.id,
                created_at=datetime.now(),
                content=content,
            ),
            context,
        )




def create_chatkit_server() -> SoftwareAIAgentServer | None:
    """Return a configured ChatKit server instance if dependencies are available."""
    # return SoftwareAIAgentServer()
    try:
        

        with app.app_context():
            db.create_all()
            logging.info("Database tables checked and created if they did not exist.")

        store_instance = PostgresStore(database=db)
        return SoftwareAIAgentServer(store=store_instance)
    except Exception as e:
        # Log and return None if store or server creation fails due to missing dependencies
        logging.error(f"Failed to create ChatKit server with PostgresStore: {e}")
        return None