import base64
import os
os.chdir(os.path.join(os.path.dirname(__file__)))

with open("docker-compose.yml", "rb") as f:
    encoded = base64.b64encode(f.read())
    print(encoded.decode())
