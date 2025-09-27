import requests
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))


API_URL = "http://localhost:5920/api/prai/gen"

API_TOKEN = "WBYZIJ3-HCxGandUwpa96l_XlEf1TbYY2oY-4mtL-Hw"
REPOSITORY = "ualers2/SoftwareAI"  
PR_NUMBER = 92
EMAIL = "freitasalexandre815@gmail.com"
PASSWORD = "teste"

payload = {
    "repository": REPOSITORY,
    "pr_number": PR_NUMBER,
    "email": EMAIL,
    "password": PASSWORD,
}

headers = {
    "Content-Type": "application/json",
    "X-API-TOKEN": API_TOKEN,
}

def testar_endpoint():
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        print("Status Code:", response.status_code)
        print("Resposta JSON:", response.json())
    except Exception as e:
        print("Erro ao chamar o endpoint:", str(e))

if __name__ == "__main__":
    testar_endpoint()
