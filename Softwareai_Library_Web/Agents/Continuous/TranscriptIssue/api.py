import json
from flask import *
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from agents import Agent, ItemHelpers,  ModelSettings, function_tool, Runner, handoff, RunContextWrapper
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, stream_with_context
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hmac
import hashlib
import threading
import asyncio
import httpx
import sys
import logging
from contextlib import suppress

import requests
from openai.types.responses import ResponseTextDeltaEvent

app = Flask(__name__)
CORS(app)  
app.secret_key = os.urandom(24)  


# Configura o logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # ou INFO, WARNING etc.

# Cria um handler para a saída padrão (stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Formato dos logs
formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Evita adicionar múltiplos handlers
if not logger.hasHandlers():
    logger.addHandler(handler)

load_dotenv(dotenv_path="keys.env")
os.environ["AGENTS_DISABLE_TRACING"] = "1"


def valid(GITHUB_WEBHOOK_SECRET_CodeReview, signature, payload):
    computed_signature = 'sha256=' + hmac.new(
        GITHUB_WEBHOOK_SECRET_CodeReview.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    Payloaddecode = payload.decode('utf-8', errors='ignore')
    logger.info(f"Signature from GitHub: {signature}")
    logger.info(f"Computed Signature: {computed_signature}")

    if not hmac.compare_digest(signature, computed_signature):
        return "Assinatura inválida", 403

    try:
        data = json.loads(payload)
        return data
    except json.JSONDecodeError:
        return "Payload inválido", 400

@app.route('/api/TranscriptIssue', methods=['POST'])
def api_TranscriptIssue():
    GITHUB_WEBHOOK_SECRET_CodeReview = os.getenv("GITHUB_WEBHOOK_SECRET")
    github_token = os.getenv("github_token")

    signature = request.headers.get('X-Hub-Signature-256')
    payload = request.data
    data = valid(GITHUB_WEBHOOK_SECRET_CodeReview, signature, payload)

    if 'zen' in data:
        return "Ping recebido", 200
    
    action = data['action']
    if action == "labeled":
        return "Ping recebido", 200
    elif action == "unlabeled":
        return "Ping recebido", 200
    elif action == "edited":
        return "Ping recebido", 200
    elif action == "closed":
        return "Ping recebido", 200
    
    issue_data = data['issue']
    issue_number = issue_data['number']
    repository_url = issue_data["repository_url"]
    repository_url_str = f"{repository_url}"
    repository_url_replace = repository_url_str.replace("https://api.github.com/repos/", "")
    repo_owner, repo_name = repository_url_replace.split("/")

    try:
        comment = data["comment"]
        autor_comentario = comment["user"]["login"]
        if str(autor_comentario) == 'QuantummCore':
            response_message = {"status": "status"}
            return jsonify(response_message), 200
        comentario_recebido = comment["body"]
    except:
        autor_comentario = issue_data["user"]["login"]
        comentario_recebido = issue_data["body"]


    logger.info(f"Comentario PR: {comentario_recebido}")
    logger.info(f"Autor: {autor_comentario}")
    logger.info(f"Issue Number: {issue_number}")



    # if str(autor_comentario) == 'ualers2':
    #     response_message = {
    #         "status": "status"
    #     }
    #     return jsonify(response_message), 200

    path_metadata = os.path.join(os.path.dirname(__file__), "metadata.json")
    with open(path_metadata, encoding='utf-8') as f:
        meta = json.load(f)
        instruction_property = meta.get("instruction_property")
        instruction_path = meta.get("instruction_path")
        model_agent = meta.get("model")
        tools_agent = meta.get("tools")
        name_agent = meta.get("name")
        instrucao = open(meta["instruction_path"], encoding='utf-8').read()


    # path_instruction = os.path.join(os.path.dirname(__file__), instruction_path)
    # with open(path_instruction, 'r', encoding='utf-8') as f:
    #     instruction_original = f.read()


    async def generate_response():
        with app.app_context():
            triage_agent = Agent(name=meta["name"],
                                instructions=instrucao,
                                model=meta["model"])
            result = Runner.run_streamed(triage_agent, comentario_recebido)

            already_sent = False
            async for event in result.stream_events():
                # We'll ignore the raw responses event deltas
                if event.type == "raw_response_event":
                    continue
                # When the agent updates, print that
                elif event.type == "agent_updated_stream_event":
                    logger.info(f"Agent updated: {event.new_agent.name}")
                    continue
                # When items are generated, print them

                elif event.type == "run_item_stream_event" and not already_sent:
                    if event.item.type == "message_output_item":
                        resposta = ItemHelpers.text_message_output(event.item)
                        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues/{issue_number}/comments"
                        headers = {
                            "Authorization": f"Bearer {github_token}",
                            "Accept": "application/vnd.github+json"
                        }
                        async with httpx.AsyncClient() as client:
                            resp = await client.post(url, headers=headers, json={"body": resposta})
                            logger.info(f"GitHub API: {resp.status_code}")
                            already_sent = True  # marca que já foi enviado
                            return jsonify({"status": "ok"}), 200


        # response_message = {
        #     "status": "true",
        #     "response": f"{result.final_output}",

        # }
        # return jsonify(response_message), 200

    def run_async():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(generate_response())
        task.add_done_callback(lambda t: loop.call_soon_threadsafe(loop.stop))
        try:
            loop.run_forever()
        finally:
            pending = [t for t in asyncio.all_tasks(loop) if not t.done()]
            for t in pending:
                t.cancel()
                with suppress(asyncio.CancelledError):
                    loop.run_until_complete(t)
            loop.close()

    threading.Thread(target=run_async, daemon=True).start()
    return jsonify({"status": "true"}), 200



if __name__ == '__main__':


    os.chdir(os.path.join(os.path.dirname(__file__)))

    app.run(host='0.0.0.0', port=129)
