## 🧠 Instrução para o Agent QA | Autonomous Unittest User Checkout by ui
**Objetivo:**         
Validar a usabilidade da funcionalidade de Compra via Checkout com integração stripe no website esta funcionando conforme esperado

## 🔍 Etapas obrigatórias
**você deve obrigatoriamente** executar na ordem abaixo:
### 1 Executar `fetch_dom`  
- url: {API_BASE_URL}/plan/prolight/checkout

### 2 Executar `gere um script Selenium`  
Com base no HTML obtido no passo 1, gere um script Selenium python que:
    0) abre o selenium em modo nao handless
    2) localize o campo de email (id/name/text)
    3) digite {email}
    2) localize o campo de senha (id/name/text)
    3) digite {password}
    4) selecione o metodo de pagamento stripe
    5) clique no botão de compra
    6) aguarda 30 segundos
    7) Realiza o processo de simulação de dados do checkout (utilize o codigo abaixo sempre pois essa parte do checkout vem diretamente da stripe e nunca muda)
 
        driver.find_element(By.ID, "email").send_keys(email)
        time.sleep(3)
 
        driver.find_element(By.ID, "cardNumber").send_keys("4242 4242 4242 4242")
        time.sleep(3)
 
        driver.find_element(By.ID, "cardExpiry").send_keys("12 / 26")
        time.sleep(3)
 
        driver.find_element(By.ID, "cardCvc").send_keys("424")
        time.sleep(3)
 
        driver.find_element(By.ID, "billingName").send_keys("Brian")
        time.sleep(5)
 
        driver.find_element(By.CSS_SELECTOR, 'button[data-testid="hosted-payment-submit-button"]').click()   
        time.sleep(40)
 
    7) Verifica se o usuário Fez o upgrade no Firebase:

        # Verifica se o redirecionamento foi para /checkout/success
        current_url = driver.current_url
        if "/checkout/success" in current_url or "/checkout/sucess" in current_url :
            # Verifica se a transação foi bem-sucedida no Firebase
            email_safe = email.replace('.', '_')
            ref = db.reference(f'users/{{email_safe}}', app=app_instance)
            user_data = ref.get()

            SUBSCRIPTION_PLAN = user_data.get("SUBSCRIPTION_PLAN")

            if user_data and user_data.get("email") == email:
                if SUBSCRIPTION_PLAN == "premium":
                    return {{
                        "success": True,
                        "message": "✅ Pagamento realizado com sucesso e usuário atualizado para o plano premium no Firebase",

                    }}
            else:
                return {{
                    "success": False,
                    "message": "⚠️ Falha no pagamento ou no registro do usuário no Firebase",
                    "firebase_path": f"users/{{email_safe}}",
                    "user_data": user_data
                }}
        else:
            driver.quit()
            delete_app(app_instance) 
            return {{
                "success": False,
                "message": "⚠️ Redirecionamento falhou. Usuário não foi direcionado para /checkout/success."
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
    "message": "✅ Pagamento realizado com sucesso e usuário atualizado para o plano premium no Firebase"
}}       

