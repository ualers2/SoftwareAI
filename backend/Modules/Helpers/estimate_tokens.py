# Back-End\Modules\Helpers\estimate_tokens.py
from datetime import datetime, timedelta
from Models.postgreSQL import db, User

# Modules/Helpers/estimate_tokens.py
import logging

try:
    import tiktoken
except Exception as e:
    raise ImportError("tiktoken não está instalado. Rode: pip install tiktoken") from e

logger = logging.getLogger(__name__)

# Mapeie aqui os limites de contexto dos modelos que você usa.
# Ajuste conforme necessário — valores conservadores por padrão.
MODEL_MAX_TOKENS = {
    "gpt-4.1-nano": 8192,
    "gpt-5-nano": 8192,
    "gpt-4o": 65536,
    "gpt-4o-mini": 65536,
    "gpt-5": 32768,
    "gpt-4": 8192,
    # adicione/ajuste conforme seus modelos
}

def _get_encoding_for_model(model: str):
    """
    Retorna o encoding tiktoken para o model; em caso de erro, usa cl100k_base.
    """
    try:
        return tiktoken.encoding_for_model(model)
    except Exception:
        logger.debug(f"Não foi possível obter encoding específico para '{model}', usando 'cl100k_base' como fallback.")
        return tiktoken.get_encoding("cl100k_base")


def estimate_tokens_from_text(text: str, model: str = "gpt-4.1-nano") -> int:
    """
    Conta tokens usando tiktoken com o encoding do modelo.
    Retorna inteiro >= 1.
    """
    if not text:
        return 1
    enc = _get_encoding_for_model(model)
    tokens = len(enc.encode(text))
    return max(1, int(tokens))


def estimate_required_tokens_for_run(
    text: str,
    model: str = "gpt-4.1-nano",
    output_ratio: float = 0.30,
    min_output_tokens: int = 50,
    safety_margin: float = 0.10,
) -> tuple[int, int, int]:
    """
    Estima:
      - input_tokens (baseados no texto)
      - est_output_tokens (chute sensato para output)
      - required_tokens_estimate = (input + output) * (1 + safety_margin)

    Usa MODEL_MAX_TOKENS para não extrapolar o contexto do modelo.
    Retorna (input_tokens, est_output_tokens, required_tokens_estimate)
    """
    input_tokens = estimate_tokens_from_text(text, model)
    max_ctx = MODEL_MAX_TOKENS.get(model, 8192)

    # espaço disponível para saída (conservador)
    available_for_output = max(0, max_ctx - input_tokens)

    # chute base proporcional
    est_output = max(min_output_tokens, int(input_tokens * output_ratio))

    # não ultrapassar o espaço disponível
    if available_for_output > 0:
        est_output = min(est_output, available_for_output)
    else:
        # já extrapolou o contexto; definir um mínimo razoável (só para checagem de cota)
        est_output = min_output_tokens

    required = int((input_tokens + est_output) * (1 + safety_margin))
    return input_tokens, est_output, required


input_tokens, est_output, required = estimate_required_tokens_for_run(
    'diff longo "Falha ao consumir tokens"',

)
print(input_tokens)
print(est_output)
print(required)



