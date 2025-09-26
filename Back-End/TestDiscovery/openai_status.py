import requests
import os
from dotenv import load_dotenv

# Carregar .env
os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../',  'Keys', 'keys.env'))

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
print(OPENAI_API_KEY)

def test_openai_status():
    try:
        response = requests.get(
            'https://api.openai.com/v1/models',
            headers={'Authorization': f'Bearer {OPENAI_API_KEY}'},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ OpenAI API está online.")
            return True
        else:
            print(f"⚠️ OpenAI API respondeu com status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro ao conectar na OpenAI API: {e}")
        return False

if __name__ == "__main__":
    test_openai_status()
