import hashlib
import hmac
def verify_signature(payload_body, signature_header, GITHUB_WEBHOOK_SECRET):
    """
    Verifica X-Hub-Signature-256 (ex: 'sha256=abcdef...').
    Retorna True se válido, False caso contrário.
    """
    if not signature_header:
        return False
    try:
        algo, signature = signature_header.split("=", 1)
    except ValueError:
        return False

    try:
        digestmod = getattr(hashlib, algo)
    except AttributeError:
        return False

    mac = hmac.new(GITHUB_WEBHOOK_SECRET.encode(), msg=payload_body, digestmod=digestmod)
    expected = mac.hexdigest()
    return hmac.compare_digest(signature, expected)

