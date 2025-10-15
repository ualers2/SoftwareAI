"""Simple in-memory store for user facts."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Iterable, List
from uuid import uuid4


class FactStatus(str, Enum):
    """Lifecycle states for collected facts."""

    PENDING = "pending"
    SAVED = "saved"
    DISCARDED = "discarded"


@dataclass(slots=True)
class Fact:
    """Represents a single fact gathered from the conversation."""

    text: str
    status: FactStatus = FactStatus.PENDING
    id: str = field(default_factory=lambda: f"fact_{uuid4().hex[:8]}")
    created_at: datetime = field(default_factory=datetime.utcnow)

    def as_dict(self) -> dict[str, str]:
        """Serialize the fact for JSON responses."""
        return {
            "id": self.id,
            "text": self.text,
            "status": self.status.value,
            "createdAt": self.created_at.isoformat(),
        }


class FactStore:
    """Thread-safe helper that stores facts in memory."""

    def __init__(self) -> None:
        self._facts: Dict[str, Fact] = {}
        self._order: List[str] = []
        self._lock = asyncio.Lock()

    async def create(self, *, text: str) -> Fact:
        """Create a pending fact and return it."""
        async with self._lock:
            fact = Fact(text=text)
            self._facts[fact.id] = fact
            self._order.append(fact.id)
            return fact

    async def mark_saved(self, fact_id: str) -> Fact | None:
        """Mark the given fact as saved, returning the updated record."""
        async with self._lock:
            fact = self._facts.get(fact_id)
            if fact is None:
                return None
            fact.status = FactStatus.SAVED
            return fact

    async def discard(self, fact_id: str) -> Fact | None:
        """Discard the fact and remove it from the active list."""
        async with self._lock:
            fact = self._facts.get(fact_id)
            if fact is None:
                return None
            fact.status = FactStatus.DISCARDED
            return fact

    async def list_saved(self) -> List[Fact]:
        """Return saved facts in insertion order."""
        async with self._lock:
            return [
                self._facts[fact_id]
                for fact_id in self._order
                if self._facts[fact_id].status == FactStatus.SAVED
            ]

    async def get(self, fact_id: str) -> Fact | None:
        async with self._lock:
            return self._facts.get(fact_id)

    async def iter_pending(self) -> Iterable[Fact]:
        async with self._lock:
            return [fact for fact in self._facts.values() if fact.status == FactStatus.PENDING]


fact_store = FactStore()
"""Global instance used by the API and the ChatKit workflow."""
