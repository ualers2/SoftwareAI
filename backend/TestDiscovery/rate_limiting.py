import requests
import os
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../', 'Keys', 'keys.env'))

OPENAI_KEY = os.getenv('OPENAI_KEY')

r = requests.post(
  "https://api.openai.com/v1/responses",
  headers={"Authorization": f"Bearer {OPENAI_KEY}"},
  json={"input":"oi"}
)
print(r.headers.get("x-ratelimit-remaining-requests"))
print(r.headers.get("x-ratelimit-remaining-tokens"))
