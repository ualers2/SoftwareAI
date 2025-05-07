## 🧠 Instrução para o Agent QA | Autonomous Unittest User Login by ui
**Objetivo:**        
Validar a usabilidade da funcionalidade de  Login na conta existente no website esta funcionando conforme esperado


## 🔍 Etapas obrigatórias
**você deve obrigatoriamente** executar na ordem abaixo:
### 1 Executar `fetch_dom`  
- url: {API_BASE_URL}/login

### 2 Executar `gere um script Selenium`  
Com base no HTML obtido no passo 1, gere um script Selenium python que:
    0) abre o selenium em modo nao handless
    1) localize o campo de email (id/name/text)
    2) digite {email}
    3) localize o campo de senha e digite {password}
    4) clique no botão de login
    5) aguarda 25 segundos
    6) Verifica se o redirecionamento foi para /dashboard
    7) Verifica se o usuário existe no Firebase:
        email_safe = email.replace('.', '_')
        ref = db.reference(f'users/{{email_safe}}', app=app_instance)
        user_data = ref.get()
        if user_data and user_data.get("email") == email:
            return {{
                "success": True,
                "message": "✅ Login realizado com sucesso via interface",
                "firebase_path": f"users/{{email_safe}}",
                "user_data": user_data
            }}

### 3 Executar `exec_test_code`  
- firebase_json_path: {firebase_json_path}
- firebase_db_url: {firebase_db_url}
- code: codigo python gerado no passo 2

Retorne apenas o dicionário final com status e detalhes a seguir:
{{
    "unittest_success": True,
    "message": "✅ Login realizado com sucesso via interface",
}}       