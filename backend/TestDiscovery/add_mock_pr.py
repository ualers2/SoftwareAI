# scripts/add_mock_pr.py
from Models.postgreSQL import db, User, PullRequest
from api import app

def add_mock_pr(email: str):
    with app.app_context():
        # Procura usuário pelo email
        user = User.query.filter_by(email=email).first()
        if not user:
            # Cria usuário mock caso não exista
            user = User(email=email, username="testuser")
            user.set_password("123456")
            db.session.add(user)
            db.session.commit()
            print(f"Usuário mock criado: {email} (id={user.id})")
        else:
            print(f"Usuário existente encontrado: {email} (id={user.id})")
        
        # Cria PR mock
        pr = PullRequest(
            user_id=user.id,
            author='AI',
            pr_number=1003,
            title="Mock Pull Request para process",
            body="Este é um PR de process gerado pelo script mock.",
            ai_generated_content="Conteúdo gerado pela IA para process",
            original_diff="diff --git a/file.txt b/file.txt\n+ linha adicionada\n- linha removida",
            status="completed",
            diff_url="https://github.com/mock/repo/pull/1003",
            processed_by="AI"
        )
        db.session.add(pr)
        db.session.commit()
        print(f"Pull Request mock criado: #{pr.pr_number} para usuário {email}")

if __name__ == "__main__":
    test_email = "freitasalexandre810@gmail.com"  # altere para o email que quiser testar
    add_mock_pr(test_email)
