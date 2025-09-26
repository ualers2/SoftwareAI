# Back-End\Modules\Resolvers\pr_process.py
import asyncio
import requests
import logging
from datetime import datetime, timedelta

from Modules.Updaters.pr_body import update_pr_body
from Modules.Updaters.pr_merge import merge_pull_request
from Modules.Geters.pr_diff import fetch_pr_diff_via_api


from Modules.Helpers.estimate_tokens import estimate_required_tokens_for_run
from Modules.Updaters.user_tokens import consume_user_tokens
from Modules.Geters.user_by_access_token import get_user_by_access_token

from Agents.PrSumary.ai import PrGen
from Models.postgreSQL import *
from Modules.Resolvers.user_identifier import *


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_pull_request(
                        app,
                        user_id,
                        GITHUB_TOKEN,
                        OPENAI_API_KEY,
                        logs_collection,
                        pr_number, 
                        repository='', 
                        model="gpt-5-nano",
                        merge=True,
                    ):
    try:
        with app.app_context():
            user = User.query.get(user_id)

            if not user:
                logger.info(f"Usuário {user_id} não encontrado. Abortando PR {pr_number}.")
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "WARNING",
                    "details": {"message": "Usuário não encontrado - quota/permissaos", "pr_number": pr_number},
                    "action": "pr_process_quota",
                    "user_id": user_id,
                    "prNumber": pr_number
                })
                return

            revoked, reason = is_token_revoked_or_expired(user)
            if revoked:
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "ERROR",
                    "details": {"message": f"Token inválido: {reason}", "pr_number": pr_number},
                    "action": "pr_process_token_invalid",
                    "user_id": user_id,
                    "prNumber": pr_number
                })
                pr = PullRequest(
                    user_id=user_id,
                    author=repository.split("/")[0] if repository else None,
                    pr_number=pr_number,
                    title="Erro: token inválido",
                    body="Processamento interrompido: token inválido ou expirado.",
                    status="error",
                )
                db.session.add(pr)
                db.session.commit()
                return

            diff_url = f"https://api.github.com/repos/{repository}/pulls/{pr_number}/files"
            diff_content = fetch_pr_diff_via_api(diff_url, GITHUB_TOKEN) or ""
            
            est_input_tokens, est_output_tokens_guess, required_tokens_estimate = estimate_required_tokens_for_run(
                diff_content, model=model, output_ratio=0.30, min_output_tokens=50, safety_margin=0.10
            )

            ok, remaining = check_user_quota(user, required_tokens_estimate)
            if not ok:
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "ERROR",
                    "details": {"message": "Saldo de tokens insuficiente", "required": required_tokens_estimate, "remaining": remaining},
                    "action": "pr_process_insufficient_tokens",
                    "user_id": user_id,
                    "prNumber": pr_number
                })
                pr = PullRequest(
                    user_id=user_id,
                    author=repository.split("/")[0] if repository else None,
                    pr_number=pr_number,
                    title="Erro: tokens insuficientes",
                    body=f"Processamento interrompido: tokens insuficientes. Requerido ≈ {required_tokens_estimate}, restante {remaining}.",
                    status="error",
                )
                db.session.add(pr)
                db.session.commit()
                return

            title, generated_pr_content, total_input_tokens, total_cached_tokens, total_reasoning_tokens, total_output_tokens, total_total_tokens = asyncio.run(
                PrGen(content_pr=diff_content, model=model, user_id=user_id, OPENAI_API_KEY=OPENAI_API_KEY)
            )

            if title == "" or title is None:
                title = "Sem Titulo"

            try:
                user.tokens_used = (user.tokens_used or 0) + int(total_total_tokens)
                db.session.add(user)
                db.session.commit()
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "INFO",
                    "details": {
                        "message": f"Tokens consumidos {total_total_tokens}",
                        "amount": total_total_tokens,
                        "remaining": (user.limit_monthly_tokens - user.tokens_used)
                    },
                    "action": "pr_process_tokens_consumed",
                    "user_id": user_id,
                    "prNumber": pr_number
                })
            except Exception as e:
                db.session.rollback()
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "ERROR",
                    "details": {"message": "Falha ao consumir tokens", "error": e},
                    "action": "pr_process_token_consume_error",
                    "user_id": user_id,
                    "prNumber": pr_number
                })


            update_pr_body(GITHUB_TOKEN, f"https://api.github.com/repos/{repository}/pulls/{pr_number}", title, generated_pr_content)
            if merge:
                merge_pull_request(GITHUB_TOKEN, repository, pr_number)

            preview = generated_pr_content[:39]
            author_name = repository.split("/")[0] if repository else None

            log_entry = {
                "timestamp": datetime.utcnow(),
                "level": "INFO",
                "details": {
                    'message': f'{preview}',
                    'processed_by': 'AI',
                    'status': 'completed',
                    'diff_url': diff_url,
                    'repository': repository,
                    'pr_url': f'https://github.com/{repository}/pull/{pr_number}',
                    'pr_number': pr_number,
                    'title': title,
                    'ai_generated_content': generated_pr_content,
                    'original_diff': diff_content,
                    'model': model,
                    'tokens_used': total_total_tokens
                },
                "action": "pr_process",
                "user_id": user_id,
                "prNumber": pr_number
            }
            result = logs_collection.insert_one(log_entry)
            print(f"✅ Log inserido com _id: {result.inserted_id}")
            
            pr = PullRequest.query.filter_by(user_id=user_id, pr_number=pr_number).first()
            if pr:
                pr.author = author_name
                pr.title = title
                pr.body = generated_pr_content
                pr.ai_generated_content = generated_pr_content
                pr.original_diff = diff_content
                pr.status = "completed"
                pr.diff_url = diff_url
                pr.processed_by = "AI"
                pr.total_tokens = total_total_tokens
            else:
                pr = PullRequest(
                    user_id=user_id,
                    author=author_name,
                    pr_number=pr_number,
                    title=title,
                    body=generated_pr_content,
                    ai_generated_content=generated_pr_content,
                    original_diff=diff_content,
                    status="completed",
                    diff_url=diff_url,
                    processed_by="AI",
                    total_tokens=total_total_tokens
                )
                db.session.add(pr)

            db.session.commit()

    except requests.exceptions.RequestException as e:
        logger.info(f"Erro ao buscar diff para PR #{pr_number}: {e}")
    except Exception as e:
        logger.info(f"Erro inesperado no processamento do PR #{pr_number}: {e}")




        