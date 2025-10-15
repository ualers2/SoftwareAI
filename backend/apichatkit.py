"""FastAPI entrypoint wiring the ChatKit server and REST endpoints."""

from __future__ import annotations
import os
from typing import Any
from dotenv import load_dotenv
from chatkit.server import StreamingResult
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import Response, StreamingResponse
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from Modules.ChatKit.chat import (
    SoftwareAIAgentServer,
    create_chatkit_server,
)
from Modules.ChatKit.facts import fact_store
from api import db, app as app_flask


os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "Keys", 'keys.env'))


app = FastAPI(title="ChatKit API")
origins = [
    "http://localhost:4684", 
    "http://localhost:5170",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

_chatkit_server: SoftwareAIAgentServer | None = create_chatkit_server()


def get_chatkit_server() -> SoftwareAIAgentServer:
    if _chatkit_server is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "ChatKit dependencies are missing. Install the ChatKit Python "
                "package to enable the conversational endpoint."
            ),
        )
    return _chatkit_server


@app.post("/chatkit")
async def chatkit_endpoint(
    request: Request, server: SoftwareAIAgentServer = Depends(get_chatkit_server)
) -> Response:
    payload = await request.body()
    result = await server.process(payload, {"request": request})
    if isinstance(result, StreamingResult):
        return StreamingResponse(result, media_type="text/event-stream")
    if hasattr(result, "json"):
        return Response(content=result.json, media_type="application/json")
    return JSONResponse(result)


@app.get("/facts")
async def list_facts() -> dict[str, Any]:
    with app_flask.app_context():
        facts = await fact_store.list_saved()
        return {"facts": [fact.as_dict() for fact in facts]}


@app.post("/facts/{fact_id}/save")
async def save_fact(fact_id: str) -> dict[str, Any]:
    with app_flask.app_context():
        fact = await fact_store.mark_saved(fact_id)
        if fact is None:
            raise HTTPException(status_code=404, detail="Fact not found")
        return {"fact": fact.as_dict()}


@app.post("/facts/{fact_id}/discard")
async def discard_fact(fact_id: str) -> dict[str, Any]:
    with app_flask.app_context():
        fact = await fact_store.discard(fact_id)
        if fact is None:
            raise HTTPException(status_code=404, detail="Fact not found")
        return {"fact": fact.as_dict()}


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "healthy"}
