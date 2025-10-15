"""
AI Module

This module provides an AI class that interfaces with language models to perform various tasks such as
starting a conversation, advancing the conversation, and handling message serialization. It also includes
backoff strategies for handling rate limit errors from the OpenAI API.

Classes:
    AI: A class that interfaces with language models for conversation management and message serialization.

Functions:
    serialize_messages(messages: List[Message]) -> str
        Serialize a list of messages to a JSON string.
"""

from __future__ import annotations

import json
import logging
import os
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Any, List, Optional, Union

import backoff
import openai
import pyperclip
from fastapi import WebSocket 
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models.base import BaseChatModel
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    messages_from_dict,
    messages_to_dict,
)
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    BaseMessageChunk,
    HumanMessage,
    convert_to_messages,
    convert_to_openai_image_block,
    is_data_content_block,
    message_chunk_to_message,
)
from langchain_anthropic import ChatAnthropic
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from Agents.gpt_engineer.core.WebSocketStreamingCallbackHandler import WebSocketStreamingCallbackHandler
from Agents.gpt_engineer.core.token_usage import TokenUsageLog
from firebase_admin import App

# Type hint for a chat message
Message = Union[AIMessage, HumanMessage, SystemMessage]

# Set up logging
logger = logging.getLogger(__name__)

class AI:
    """
    A class that interfaces with language models for conversation management and message serialization.

    This class provides methods to start and advance conversations, handle message serialization,
    and implement backoff strategies for rate limit errors when interacting with the OpenAI API.

    Attributes
    ----------
    temperature : float
        The temperature setting for the language model.
    azure_endpoint : str
        The endpoint URL for the Azure-hosted language model.
    model_name : str
        The name of the language model to use.
    streaming : bool
        A flag indicating whether to use streaming for the language model.
    llm : BaseChatModel
        The language model instance for conversation management.
    token_usage_log : TokenUsageLog
        A log for tracking token usage during conversations.

    Methods
    -------
    start(system: str, user: str, step_name: str) -> List[Message]
        Start the conversation with a system message and a user message.
    next(messages: List[Message], prompt: Optional[str], step_name: str) -> List[Message]
        Advances the conversation by sending message history to LLM and updating with the response.
    backoff_inference(messages: List[Message]) -> Any
        Perform inference using the language model with an exponential backoff strategy.
    serialize_messages(messages: List[Message]) -> str
        Serialize a list of messages to a JSON string.
    deserialize_messages(jsondictstr: str) -> List[Message]
        Deserialize a JSON string to a list of messages.
    _create_chat_model() -> BaseChatModel
        Create a chat model with the specified model name and temperature.
    """

    def __init__(
        self,
        model_name="gpt-4-turbo",
        temperature=0.1,
        azure_endpoint=None,
        streaming=True,
        vision=False,
        ActiveWebSocket: Optional[WebSocket] = None,
        session_id: Optional[str] = None,
        user_email: Optional[str] = None,
        appcompany: Optional[App] = None,
    ):
        """
        Initialize the AI class.

        Parameters
        ----------
        model_name : str, optional
            The name of the model to use, by default "gpt-4".
        temperature : float, optional
            The temperature to use for the model, by default 0.1.
        """
        self.ActiveWebSocket = ActiveWebSocket
        self.session_id=session_id
        self.user_email=user_email
        self.appcompany=appcompany
        self.temperature = temperature
        self.azure_endpoint = azure_endpoint
        self.model_name = model_name
        self.streaming = streaming
        self.vision = (
            ("vision-preview" in model_name)
            or ("gpt-4-turbo" in model_name and "preview" not in model_name)
            or ("claude" in model_name)
        )
        self.llm = self._create_chat_model()
        self.llm_with_tools = self.llm.bind_tools([AutosaveTool])
        self.structured_llm = self.llm.with_structured_output(DiffOutput)

        self.token_usage_log = TokenUsageLog(model_name)
        print(f"Using model {self.model_name}")
        logger.debug(f"Using model {self.model_name}")

    def start(self, system: str, user: Any, *, step_name: str) -> List[Message]:
        """
        Start the conversation with a system message and a user message.

        Parameters
        ----------
        system : str
            The content of the system message.
        user : str
            The content of the user message.
        step_name : str
            The name of the step.

        Returns
        -------
        List[Message]
            The list of messages in the conversation.
        """

        messages: List[Message] = [
            SystemMessage(content=system),
            HumanMessage(content=user),
        ]
        return self.next(messages, step_name=step_name)

    def next(
        self,
        messages: List[Message],
        prompt: Optional[str] = None,
        tools: bool = False,
        structured_output: bool = False,
        *,
        step_name: str,
    ) -> List[Message]:
        """
        Advances the conversation by sending message history
        to LLM and updating with the response.

        Parameters
        ----------
        messages : List[Message]
            The list of messages in the conversation.
        prompt : Optional[str], optional
            The prompt to use, by default None.
        step_name : str
            The name of the step.

        Returns
        -------
        List[Message]
            The updated list of messages in the conversation.
        """

        if prompt:
            messages.append(HumanMessage(content=prompt))

        logger.debug(
            "Creating a new chat completion: %s",
            # "\n".join([m.pretty_repr() for m in messages]),
        )

        if not self.vision:
            messages = self._collapse_text_messages(messages)

        if tools == True:
            response, content = self.backoff_inference(messages, tools=True)
        elif structured_output == True:
            response, content = self.backoff_inference(messages, structured_output=True)
        else:    
            response, content = self.backoff_inference(messages)

        self.token_usage_log.update_log(
            messages=messages, answer=content, step_name=step_name
        )
        messages.append(response)
        logger.debug(f"Chat completion finished: {messages}")

        return messages

    @backoff.on_exception(backoff.expo, openai.RateLimitError, max_tries=7, max_time=45)
    def backoff_inference(self, messages, tools=False, structured_output=False):
        """
        Perform inference using the language model while implementing an exponential backoff strategy.

        This function will retry the inference in case of a rate limit error from the OpenAI API.
        It uses an exponential backoff strategy, meaning the wait time between retries increases
        exponentially. The function will attempt to retry up to 7 times within a span of 45 seconds.

        Parameters
        ----------
        messages : List[Message]
            A list of chat messages which will be passed to the language model for processing.

        callbacks : List[Callable]
            A list of callback functions that are triggered after each inference. These functions
            can be used for logging, monitoring, or other auxiliary tasks.

        Returns
        -------
        Any
            The output from the language model after processing the provided messages.

        Raises
        ------
        openai.error.RateLimitError
            If the number of retries exceeds the maximum or if the rate limit persists beyond the
            allotted time, the function will ultimately raise a RateLimitError.

        Example
        -------
        >>> messages = [SystemMessage(content="Hello"), HumanMessage(content="How's the weather?")]
        >>> response = backoff_inference(messages)
        """
        if tools == True:
            tool_results = []
            response_inference = self.llm_with_tools.invoke(messages)  
            logger.info(f"Tool calls retornadas pelo LLM: {response_inference.tool_calls}")
            for tool_call in getattr(response_inference, "tool_calls", []):
                tool_name = tool_call.get("name")
                args = tool_call.get("args", {})
                if tool_name == "AutosaveTool":
                    result = self.autosave(AutosaveTool(**args))
                    logger.info(f"Resultado da tool:{result}")
                    tool_results.append(result)
            content_str = f"Tool calls retornadas pelo LLM: {response_inference.tool_calls}\n All Response Tools: {tool_results}"
            response = BaseMessage(type="ai", content=content_str)
            content = response.content
            return response, content
        elif structured_output == True:
            response_inference = self.structured_llm.invoke(messages) 
            diff = response_inference.diff
            filename = response_inference.filename
            content_str = f"{filename}\n{diff}"
            response = BaseMessage(type="ai", content=content_str)
            content = response.content
            return response, content
        else:
            response = self.llm.invoke(messages) 
            content = response.content
            return response, content

    @staticmethod
    def serialize_messages(messages: List[Message]) -> str:
        """
        Serialize a list of messages to a JSON string.

        Parameters
        ----------
        messages : List[Message]
            The list of messages to serialize.

        Returns
        -------
        str
            The serialized messages as a JSON string.
        """
        return json.dumps(messages_to_dict(messages))

    @staticmethod
    def deserialize_messages(jsondictstr: str) -> List[Message]:
        """
        Deserialize a JSON string to a list of messages.

        Parameters
        ----------
        jsondictstr : str
            The JSON string to deserialize.

        Returns
        -------
        List[Message]
            The deserialized list of messages.
        """
        data = json.loads(jsondictstr)
        # Modify implicit is_chunk property to ALWAYS false
        # since Langchain's Message schema is stricter
        prevalidated_data = [
            {**item, "tools": {**item.get("tools", {}), "is_chunk": False}}
            for item in data
        ]
        return list(messages_from_dict(prevalidated_data))  # type: ignore

    def _create_chat_model(self) -> BaseChatModel:
        """
        Create a chat model with the specified model name and temperature.

        Parameters
        ----------
        model : str
            The name of the model to create.
        temperature : float
            The temperature to use for the model.

        Returns
        -------
        BaseChatModel
            The created chat model.
        """
        if self.ActiveWebSocket == None:
            callhandler_ = StreamingStdOutCallbackHandler()
        else:
            callhandler_ = WebSocketStreamingCallbackHandler(
                websocketactivedstream=self.ActiveWebSocket,
                session_id=self.session_id,
                user_email=self.user_email,
                appcompany=self.appcompany
                                                             
                )


                    
        if self.azure_endpoint:
            return AzureChatOpenAI(
                azure_endpoint=self.azure_endpoint,
                openai_api_version=os.getenv(
                    "OPENAI_API_VERSION", "2024-05-01-preview"
                ),
                deployment_name=self.model_name,
                openai_api_type="azure",
                streaming=self.streaming,
                callbacks=[callhandler_],
            )
        elif "claude" in self.model_name:
            return ChatAnthropic(
                model=self.model_name,
                temperature=self.temperature,
                callbacks=[callhandler_],
                streaming=self.streaming,
                max_tokens_to_sample=4096,
            )
        elif self.vision:
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                streaming=self.streaming,
                callbacks=[callhandler_],
                max_tokens=4096,  # vision models default to low max token limits
            )
        else:
            return ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                streaming=self.streaming,
                callbacks=[callhandler_],
            )

    def autosave(self, data: AutosaveTool) -> dict:
        """Função que salva o código, chamada pela tool do LLM"""
        try:
            os.makedirs(os.path.dirname(data.path), exist_ok=True)
            with open(data.path, 'w', encoding='utf-8') as f:
                f.write(data.code)
            logger.info(f"Arquivo salvo com sucesso: {data.path}")
            return {"status": "success", "file_path": data.path}
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo {data.path}: {e}")
            return {"status": "error", "message": str(e)}
        
    def _extract_content(self, content):
        """
        Extracts text content from a message, supporting both string and list types.
        Parameters
        ----------
        content : Union[str, List[dict]]
            The content of a message, which could be a string or a list.
        Returns
        -------
        str
            The extracted text content.
        """
        if isinstance(content, str):
            return content
        elif isinstance(content, list) and content and "text" in content[0]:
            # Assuming the structure of list content is [{'type': 'text', 'text': 'Some text'}, ...]
            return content[0]["text"]
        else:
            return ""

    def _collapse_text_messages(self, messages: List[Message]):
        """
        Combine consecutive messages of the same type into a single message, where if the message content
        is a list type, the first text element's content is taken. This method keeps `combined_content` as a string.

        This method iterates through the list of messages, combining consecutive messages of the same type
        by joining their content with a newline character. If the content is a list, it extracts text from the first
        text element's content. This reduces the number of messages and simplifies the conversation for processing.

        Parameters
        ----------
        messages : List[Message]
            The list of messages to collapse.

        Returns
        -------
        List[Message]
            The list of messages after collapsing consecutive messages of the same type.
        """
        collapsed_messages = []
        if not messages:
            return collapsed_messages

        previous_message = messages[0]
        combined_content = self._extract_content(previous_message.content)

        for current_message in messages[1:]:
            if current_message.type == previous_message.type:
                combined_content += "\n\n" + self._extract_content(
                    current_message.content
                )
            else:
                collapsed_messages.append(
                    previous_message.__class__(content=combined_content)
                )
                previous_message = current_message
                combined_content = self._extract_content(current_message.content)

        collapsed_messages.append(previous_message.__class__(content=combined_content))
        return collapsed_messages

class AutosaveTool(BaseModel):
    """Tool para salvar código Python em arquivo"""
    code: str = Field(..., description="Código Python a ser salvo")
    path: str = Field(..., description="Caminho completo do arquivo onde o código será salvo")

class DiffOutput(BaseModel):
    filename: str
    diff: str


def serialize_messages(messages: List[Message]) -> str:
    return AI.serialize_messages(messages)
