import os
import logging
from flask import Flask, request, abort
from dotenv import load_dotenv
import threading
from Modules.Resolvers.pr_process import process_pull_request
from Modules.Resolvers.verify_signature import verify_signature
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
load_dotenv(os.path.join(os.path.dirname(__file__), "keys.env"))
app = Flask(__name__)
GITHUB_SECRET = os.getenv('GITHUB_SECRET', '')
repo_name = os.getenv('repo_name', '')
GITHUB_TOKEN = os.getenv('github_token', '')
repo_path = os.getenv('repo_path', '')
new_name_for_html = os.getenv('new_name_for_html', '')
new_name_for_js = os.getenv('new_name_for_js', '')
new_name_for_css = os.getenv('new_name_for_css', '')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

@app.route('/webhook/genpr', methods=['POST'])
def webhookgenpr():
    model = "gpt-5-nano"

    if not verify_signature(GITHUB_SECRET, request):
        abort(403, 'Assinatura inválida')

    payload = request.get_json()
    event_type = request.headers.get('X-GitHub-Event')
    logger.info(f"Payload recebido: {payload.get('action')}, Evento: {event_type}")
    if event_type == "pull_request":
        action = payload.get("action")
        pull_request = payload.get("pull_request")
        if action in ["opened", "reopened", "synchronize"] and pull_request:
            pr_url = pull_request["url"]
            pr_diff_url = pull_request["diff_url"]
            pr_number = pull_request["number"]
            pr_title = pull_request["title"]
            pr_body = pull_request["body"]
            logger.info(f"Evento de Pull Request '{action}' recebido para PR #{pr_number}")
            threading.Thread(target=process_pull_request, args=(GITHUB_TOKEN,  pr_number, pr_url, repo_name, model, )).start()
            return 'Processamento do Pull Request iniciado', 202

    logger.info("Evento ignorado.")
    return 'Evento ignorado', 200
# if __name__ == '__main__':
#     logger.info("Inicialized !!!!!!")
#     app.run(host='0.0.0.0', port=5071)