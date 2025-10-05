# Back-End\Modules\Resolvers\commit_process.py
import asyncio
import requests
import logging
from datetime import datetime


from Modules.Helpers.estimate_tokens import estimate_required_tokens_for_run
from Modules.Updaters.user_tokens import consume_user_tokens
from Modules.Geters.user_by_access_token import get_user_by_access_token

from Agents.GitContextLayer.ai import GenerateCommitMessageAgent
from Models.postgreSQL import *
from Modules.Resolvers.user_identifier import *

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def process_git_context_layer(
                        app,
                        user_id,
                        OPENAI_API_KEY,
                        logs_collection,
                        commit_hash, 
                        diff,
                        files,
                        repository='', 
                        commit_language='pt',
                        model="gpt-5-nano",
                    ):
    try:
        with app.app_context():
            user = User.query.get(user_id)

            if not user:
                logger.info(f"Usuário {user_id} não encontrado. Abortando commit {commit_hash}.")
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "WARNING",
                    "details": {"message": "Usuário não encontrado", "commit_hash": commit_hash},
                    "action": "commit_process_quota",
                    "user_id": user_id,
                    "commit_hash": commit_hash
                })
                return

            revoked, reason = is_token_revoked_or_expired(user)
            if revoked:
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "ERROR",
                    "details": {"message": f"Token inválido: {reason}", "commit_hash": commit_hash},
                    "action": "commit_process_token_invalid",
                    "user_id": user_id,
                    "commit_hash": commit_hash
                })
                commit_entry = CommitMessage(
                    user_id=user_id,
                    author=repository.split("/")[0] if repository else None,
                    commit_hash=commit_hash,
                    message="Erro: token inválido",
                    status="error",
                )
                db.session.add(commit_entry)
                db.session.commit()
                return
            
            est_input_tokens, est_output_tokens_guess, required_tokens_estimate = estimate_required_tokens_for_run(
                diff, model=model, output_ratio=0.30, min_output_tokens=50, safety_margin=0.10
            )

            ok, remaining = check_user_quota(user, required_tokens_estimate)
            if not ok:
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "ERROR",
                    "details": {"message": "Saldo de tokens insuficiente", "required": required_tokens_estimate, "remaining": remaining},
                    "action": "commit_process_insufficient_tokens",
                    "user_id": user_id,
                    "commit_hash": commit_hash
                })
                commit_entry = CommitMessage(
                    user_id=user_id,
                    author=repository.split("/")[0] if repository else None,
                    commit_hash=commit_hash,
                    message=f"Erro: tokens insuficientes. Requerido ≈ {required_tokens_estimate}, restante {remaining}.",
                    status="error",
                )
                db.session.add(commit_entry)
                db.session.commit()
                return

            commit_message, commit_title, total_total_tokens = asyncio.run(GenerateCommitMessageAgent(
                                        diff=diff, 
                                        files=files, 
                                        model=model, 
                                        user_id=user_id,
                                        commit_language=commit_language, 
                                        OPENAI_API_KEY=OPENAI_API_KEY
                                        )
            )
            generated_message  = f"{commit_title}\n\n{commit_message}"
            
            if not generated_message:
                generated_message = "Mensagem de commit automática"

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
                    "action": "commit_process_tokens_consumed",
                    "user_id": user_id,
                    "commit_hash": commit_hash
                })
            except Exception as e:
                db.session.rollback()
                logs_collection.insert_one({
                    "timestamp": datetime.utcnow(),
                    "level": "ERROR",
                    "details": {"message": "Falha ao consumir tokens", "error": str(e)},
                    "action": "commit_process_token_consume_error",
                    "user_id": user_id,
                    "commit_hash": commit_hash
                })

            commit_entry = CommitMessage.query.filter_by(user_id=user_id, commit_hash=commit_hash).first()
            author_name = repository.split("/")[0] if repository else None

            if commit_entry:
                commit_entry.author = "AI"
                commit_entry.title = f"{commit_title}"
                commit_entry.processed_at = datetime.utcnow
                commit_entry.original_diff = diff
                # commit_entry.author = author_name
                commit_entry.message = generated_message
                commit_entry.ai_generated_message = generated_message
                commit_entry.status = "completed"
                commit_entry.processed_by = "AI"
                commit_entry.total_tokens = total_total_tokens
            else:
                commit_entry = CommitMessage(
                    user_id=user_id,
                    author="AI",
                    title=f"{commit_title}",
                    commit_hash=commit_hash,
                    message=generated_message,
                    ai_generated_message=generated_message,
                    status="completed",
                    processed_by="AI",
                    total_tokens=total_total_tokens,
                    original_diff=diff,
                    processed_at=datetime.utcnow()
                )
                db.session.add(commit_entry)

            db.session.commit()

            logs_collection.insert_one({
                "timestamp": datetime.utcnow(),
                "level": "INFO",
                "details": {
                    'message': generated_message[:39],
                    'processed_by': 'AI',
                    'status': 'completed',
                    'repository': repository,
                    'commit_hash': commit_hash,
                    'ai_generated_message': generated_message,
                    'model': model,
                    'tokens_used': total_total_tokens
                },
                "action": "commit_process",
                "user_id": user_id,
                "commit_hash": commit_hash
            })
            logger.info(f"✅ Commit processado: {commit_hash}")
            return generated_message

    except requests.exceptions.RequestException as e:
        logger.info(f"Erro ao buscar diff para commit {commit_hash}: {e}")
    except Exception as e:
        logger.info(f"Erro inesperado no processamento do commit {commit_hash}: {e}")
