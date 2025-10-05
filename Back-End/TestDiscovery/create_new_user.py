import requests

API_URL = "http://localhost:5910/api/register" 

def criar_conta(email: str, senha: str, expires_days: int = None):
    payload = {
        "email": email,
        "password": senha,
    }
    if expires_days is not None:
        payload["expires_days"] = expires_days

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        print("✅ Conta criada com sucesso!")
        print(f"User ID: {data.get('user_id')}")
        print(f"Token: {data.get('acess_token')}")
        print(f"Expira em: {data.get('expires_at')}")
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"❌ Erro HTTP: {http_err} -> {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"❌ Erro de requisição: {err}")

# Exemplo de uso
if __name__ == "__main__":
    criar_conta("teste@example.com", "minhasenha123", expires_days=30)
