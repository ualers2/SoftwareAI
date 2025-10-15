
from __future__ import annotations

from typing import Annotated, Any, AsyncIterator, Final, Literal
from chatkit.agents import AgentContext
from pydantic import ConfigDict, Field
from .memory_store import MemoryStore


class FactAgentContext(AgentContext):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    store: Annotated[MemoryStore, Field(exclude=True)]
    request_context: dict[str, Any]
