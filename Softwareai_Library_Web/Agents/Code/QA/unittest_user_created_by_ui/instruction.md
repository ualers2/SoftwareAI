

## 🧠 Instrução para o Agent QA | Autonomous Unittest User Register by ui
**Objetivo:**         
Validar a usabilidade da funcionalidade de Registrar nova conta no website esta funcionando conforme esperado

## 🔍 Etapas obrigatórias
**você deve obrigatoriamente** executar na ordem abaixo:
### 1 Executar `fetch_dom`  
- url: {API_BASE_URL}/login

### 2 Executar `gere um script Selenium`  
Com base no HTML obtido no passo 1, gere um script Selenium python que:
    0) abre o selenium em modo nao handless
    1) Navegue Até a area de registrar conta 
    2) localize o campo de email (id/name/text)
    3) digite {email}
    4) localize o campo de senha e digite {password}
    5) clique no botão de registrar
    6) aguarda 25 segundos
    7) Verifica se o usuário foi registrado no Firebase:
        email_safe = email.replace('.', '_')
        ref = db.reference(f'users/{{email_safe}}', app=app_instance)
        user_data = ref.get()
        if user_data and user_data.get("email") == email:
            return {{
                "unittest_success": True,
                "message": "✅ Usuário registrado com sucesso no Firebase"
            }}
        else:
            return {{
                "unittest_success": False,
                "message": " ⚠️ Usuário não encontrado no Firebase após o registro"
            }}
        finally:
            if driver: 
                driver.quit()
            if app_instance:
                delete_app(app_instance) 


### 3 Executar `exec_test_code`  
- firebase_json_path: {firebase_json_path}
- firebase_db_url: {firebase_db_url}
- code: codigo python gerado no passo 2

Retorne apenas o dicionário final com status e detalhes a seguir:
{{
    "unittest_success": True,
    "message": "✅ Usuário registrado com sucesso no Firebase"
}}       