"""
WebSocket AI Streaming Module

This module extends the existing AI class to support real-time token streaming via WebSocket.
It includes a custom callback handler for WebSocket streaming and an enhanced AI class.
"""

import asyncio
import json
import sys
import logging
from typing import Any, Dict, List, Optional, Union
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
import websockets
from fastapi import WebSocket 
from firebase_admin import App
# from modules.Chat.history.save_history_user import save_history_user
# from modules.Chat.history.save_history_system import save_history_system

logger = logging.getLogger(__name__)


class WebSocketStreamingCallbackHandler(BaseCallbackHandler):
    """
    Custom callback handler that streams LLM tokens to WebSocket clients in real-time.
    """
    
    def __init__(self, websocketactivedstream: WebSocket, session_id: str, user_email: str, appcompany: App):
        super().__init__()
        self.websocketactivedstream = websocketactivedstream
        self.session_id = session_id
        self.user_email = user_email
        self.appcompany = appcompany
        self.is_streaming = False
        self.buffer_system = ""
    
    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Called when LLM starts generating."""
        self.is_streaming = True
        logger.info(f"stream_start")
        await self._send_message(type="stream_start", message={
                "status": "started",
                "timestamp": asyncio.get_event_loop().time()
            }
        )
        # save_history_user(self.session_id, self.user_email, prompts, self.appcompany)

    async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Called when a new token is generated."""
        if self.is_streaming:
            await self._send_message(type="real_stream", message=f"{token}")
            self.buffer_system += token
            # sys.stdout.write(token)
            # sys.stdout.flush()

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Called when LLM finishes generating."""
        self.is_streaming = False
        await self._send_message(type="stream_end", message={
                "status": "completed",
                "timestamp": asyncio.get_event_loop().time()
            }
            )
        logger.info(f"stream_end")
        # save_history_system(self.session_id, self.user_email, self.buffer_system, self.appcompany)
        # self.buffer_system = ""


    async def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> None:
        """Called when LLM encounters an error."""
        self.is_streaming = False
        await self._send_message(type="error", message={
                "error": str(error),
                "timestamp": asyncio.get_event_loop().time()
            }
        )

    
    async def _send_message(self, type: str, message) -> None:
        """Send message to WebSocket client."""
        payload = {
            "Chat Agent": {
                "type": type,
                "message": message
            }
        }
        
        try:
            await self.websocketactivedstream.send_json(payload)
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed during streaming")
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")

