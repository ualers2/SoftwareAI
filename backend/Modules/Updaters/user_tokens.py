from Models.postgreSQL import db, User
from datetime import datetime, timedelta

def consume_user_tokens(user: User, tokens: int, app):
    """
    Incrementa tokens_used e persiste.
    Deve ser chamado dentro de app.app_context() onde necessário.
    """
    if user is None:
        return False, "Usuário inválido"
    with app.app_context():
        try:
            user.tokens_used = (user.tokens_used or 0) + int(tokens)
            db.session.add(user)
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            return False, str(e)


