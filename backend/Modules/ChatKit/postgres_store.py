# postgres_store.py
from __future__ import annotations

from datetime import datetime
import logging
import json
from typing import Any

from chatkit.store import NotFoundError, Store
from Modules.ChatKit.memory_store import MemoryStore  # opcional: manter se for subclass
from chatkit.types import Page, ThreadItem, ThreadMetadata
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.exc import NoResultFound
from sqlalchemy import and_, desc, func, or_

from chatkit.types import UserMessageItem, AssistantMessageItem, HiddenContextItem, ClientToolCallItem, ThreadItem as GenericThreadItem

from api import db, app

logging.basicConfig(level=logging.INFO)

# Serializador auxiliar — mas preferimos gravar dicts, não strings.
def json_serial(obj):
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    raise TypeError(f"Tipo {type(obj)} não é serializável em JSON")

def _validate_thread_item(raw: Any):
    """
    Tenta várias estratégias para transformar `raw` (dict) em um ThreadItem:
    1) usar ThreadItem.model_validate (se existir)
    2) usar pydantic.TypeAdapter (v2)
    3) usar pydantic.parse_obj_as (v1)
    4) tentar model_validate nas subclasses conhecidas
    5) tentar instanciar Generic ThreadItem diretamente
    Se nenhuma funcionar, lança Exception.
    """
    # 1) Se ThreadItem expuser model_validate (pydantic v2 style em classe), tenta
    try:
        validator = getattr(ThreadItem, "model_validate", None)
        if callable(validator):
            return ThreadItem.model_validate(raw)
    except Exception:
        pass

    # 2) TypeAdapter (pydantic v2)
    try:
        from pydantic import TypeAdapter
        return TypeAdapter(ThreadItem).validate_python(raw)
    except Exception:
        pass

    # 3) parse_obj_as (pydantic v1)
    try:
        from pydantic import parse_obj_as
        return parse_obj_as(ThreadItem, raw)
    except Exception:
        pass

    # 4) tentar subclasses conhecidas (defensivo)
    for cls in (UserMessageItem, AssistantMessageItem, HiddenContextItem, ClientToolCallItem):
        try:
            validator = getattr(cls, "model_validate", None)
            if callable(validator):
                return cls.model_validate(raw)
            # fallback simples para instanciar via construtor
            return cls(**raw)
        except Exception:
            continue

    # 5) último recurso: tentar criar um ThreadItem "genérico" (se existir)
    try:
        # Se ThreadItem for Union, talvez exista uma implementação base importável chamada ThreadItemBase
        base_validator = getattr(ThreadItem, "model_validate", None)
        if callable(base_validator):
            return base_validator(raw)
    except Exception:
        pass

    # Nenhuma estratégia funcionou -> levantar erro para que o caller logue e continue
    raise ValueError("Não foi possível desserializar ThreadItem com as estratégias conhecidas.")

class Thread(db.Model):
    __tablename__ = "threads"
    id = db.Column(db.String, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    thread_data = db.Column(JSONB, nullable=False)
    items = db.relationship("Item", backref="thread", lazy=True, cascade="all, delete-orphan")


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.String, primary_key=True)
    thread_id = db.Column(db.String, db.ForeignKey("threads.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    data = db.Column(JSONB, nullable=False)


class PostgresStore(MemoryStore):
    """Implementação da Store do ChatKit usando PostgreSQL/SQLAlchemy."""

    def __init__(self, database: SQLAlchemy):
        self.db = database

    # -- Threads ---------------------------------------------------------
    async def save_thread(self, thread: ThreadMetadata, context: dict[str, Any]) -> None:
        with app.app_context():
            # gravar como dict (JSONB), convertendo datetime para iso
            thread_data_dict = json.loads(json.dumps(thread.model_dump(), default=json_serial))
            thread_record = self.db.session.query(Thread).filter_by(id=thread.id).first()
            if thread_record is None:
                thread_record = Thread(
                    id=thread.id,
                    created_at=thread.created_at or datetime.utcnow(),
                    thread_data=thread_data_dict,
                )
                self.db.session.add(thread_record)
            else:
                thread_record.thread_data = thread_data_dict
                # manter created_at se já existir
            self.db.session.commit()
            # manter compatibilidade com MemoryStore (que não retorna)
            return None

    async def load_thread(self, thread_id: str, context: dict[str, Any]) -> ThreadMetadata:
        with app.app_context():
            try:
                thread_record = self.db.session.query(Thread).filter_by(id=thread_id).one()
            except NoResultFound as e:
                raise NotFoundError(f"Thread '{thread_id}' not found.") from e

            raw = thread_record.thread_data
            if isinstance(raw, str):
                try:
                    raw = json.loads(raw)
                except Exception:
                    logging.error(f"Thread {thread_id} possui JSON inválido em thread_data.")
                    raise
            return ThreadMetadata.model_validate(raw)

    async def load_threads(
        self,
        limit: int,
        after: str | None,
        order: str,
        context: dict[str, Any],
    ) -> Page[ThreadMetadata]:
        """Assinatura alinhada com MemoryStore: (limit, after, order, context)."""
        with app.app_context():
            order_by_clauses = [desc(Thread.created_at) if order == "desc" else Thread.created_at]
            order_by_clauses.append(Thread.id.desc() if order == "desc" else Thread.id.asc())

            query = self.db.session.query(Thread).order_by(*order_by_clauses)

            if after:
                try:
                    after_thread = self.db.session.query(Thread).filter_by(id=after).one()
                except NoResultFound:
                    after_thread = None

                if after_thread:
                    if order == "desc":
                        query = query.filter(
                            or_(
                                Thread.created_at < after_thread.created_at,
                                and_(
                                    Thread.created_at == after_thread.created_at,
                                    Thread.id > after_thread.id,
                                ),
                            )
                        )
                    else:
                        query = query.filter(
                            or_(
                                Thread.created_at > after_thread.created_at,
                                and_(
                                    Thread.created_at == after_thread.created_at,
                                    Thread.id < after_thread.id,
                                ),
                            )
                        )

            results = query.limit(limit + 1).all()
            has_more = len(results) > limit

            data = []
            for rec in results[:limit]:
                raw = rec.thread_data
                if isinstance(raw, str):
                    try:
                        raw = json.loads(raw)
                    except Exception:
                        logging.error(f"Thread {rec.id} possui JSON inválido em thread_data.")
                        continue
                try:
                    data.append(ThreadMetadata.model_validate(raw))
                except Exception as e:
                    logging.error(f"Falha ao validar ThreadMetadata {rec.id}: {e}")
                    continue

            next_after = data[-1].id if has_more and data else None
            return Page(data=data, has_more=has_more, after=next_after)

    async def delete_thread(self, thread_id: str, context: dict[str, Any]) -> None:
        with app.app_context():
            thread_record = self.db.session.query(Thread).filter_by(id=thread_id).first()
            if thread_record:
                self.db.session.delete(thread_record)
                self.db.session.commit()

    # -- Thread items ---------------------------------------------------
    async def add_thread_item(self, thread_id: str, item: ThreadItem, context: dict[str, Any]) -> None:
        """Adiciona item gravando um dict (JSONB), não string."""
        with app.app_context():
            item_dict = json.loads(json.dumps(item.model_dump(), default=json_serial))
            item_record = Item(
                id=item.id,
                thread_id=thread_id,
                created_at=item.created_at or datetime.utcnow(),
                data=item_dict,
            )
            self.db.session.add(item_record)
            self.db.session.commit()
            return None

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: dict[str, Any],
    ) -> Page[ThreadItem]:
        with app.app_context():
            order_by_clauses = [desc(Item.created_at) if order == "desc" else Item.created_at]
            order_by_clauses.append(Item.id.desc() if order == "desc" else Item.id.asc())

            query = (
                self.db.session.query(Item)
                .filter_by(thread_id=thread_id)
                .order_by(*order_by_clauses)
            )

            if after:
                try:
                    after_item = self.db.session.query(Item).filter_by(id=after).one()
                except NoResultFound:
                    after_item = None

                if after_item:
                    if order == "desc":
                        query = query.filter(
                            or_(
                                Item.created_at < after_item.created_at,
                                and_(Item.created_at == after_item.created_at, Item.id > after_item.id),
                            )
                        )
                    else:
                        query = query.filter(
                            or_(
                                Item.created_at > after_item.created_at,
                                and_(Item.created_at == after_item.created_at, Item.id < after_item.id),
                            )
                        )

            results = query.limit(limit + 1).all()
            has_more = len(results) > limit

            data: list[ThreadItem] = []
            for rec in results[:limit]:
                try:
                    raw = rec.data
                    # JSONB normalmente já vem como dict. Se por algum motivo for string, carregar.
                    if isinstance(raw, str):
                        raw = json.loads(raw)
                    item = _validate_thread_item(raw)
                    data.append(item)
                except Exception as e:
                    logging.error(f"Falha ao desserializar ThreadItem {rec.id}: {e}")
                    # NÃO interromper a iteração; apenas pular o item inválido.
                    continue

            next_after = data[-1].id if has_more and data else None
            return Page(data=data, has_more=has_more, after=next_after)


    async def delete_thread_item(self, thread_id: str, item_id: str, context: dict[str, Any]) -> None:
        with app.app_context():
            item = self.db.session.query(Item).filter_by(id=item_id, thread_id=thread_id).first()
            if item:
                self.db.session.delete(item)
                self.db.session.commit()

    async def save_item(self, thread_id: str, item: ThreadItem, context: dict[str, Any]) -> None:
        with app.app_context():
            item_record = self.db.session.query(Item).filter_by(id=item.id, thread_id=thread_id).first()
            item_dict = json.loads(json.dumps(item.model_dump(), default=json_serial))

            if item_record:
                item_record.data = item_dict
                item_record.created_at = item.created_at or item_record.created_at
            else:
                item_record = Item(
                    id=item.id,
                    thread_id=thread_id,
                    created_at=item.created_at or datetime.utcnow(),
                    data=item_dict,
                )
                self.db.session.add(item_record)

            self.db.session.commit()
            return None

    async def load_item(self, thread_id: str, item_id: str, context: dict[str, Any]) -> ThreadItem:
        with app.app_context():
            item_record = self.db.session.query(Item).filter_by(id=item_id, thread_id=thread_id).first()
            if not item_record:
                raise NotFoundError(f"Item '{item_id}' not found in thread '{thread_id}'")

            raw = item_record.data
            if isinstance(raw, str):
                raw = json.loads(raw)

            try:
                return _validate_thread_item(raw)
            except Exception as e:
                logging.error(f"Falha ao desserializar (load_item) ThreadItem {item_id}: {e}")
                # convertendo pra NotFound para manter contrato (ou pode re-raise dependendo do desired behavior)
                raise

    # -- Attachments (não implementado) ---------------------------------
    async def save_attachment(self, attachment, context):
        raise NotImplementedError("Anexos não são suportados.")

    async def load_attachment(self, attachment_id, context):
        raise NotImplementedError("Anexos não são suportados.")

    async def delete_attachment(self, attachment_id: str, context: dict[str, Any]) -> None:
        raise NotImplementedError("Anexos não são suportados no PostgresStore.")
