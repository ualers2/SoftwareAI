from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *


              
def CodeFlaskBackEnd_Keys_fb_STATIC(
                            user_credentials,
                            firebase_db_url,
                            session_id, appcompany,
                            path_ProjectWeb,
                            path_html,
                            path_js,
                            path_css,
                            doc_md,
                            Keys_path,
                            user_code_init_env,
                        ):

    path_credentials = f"{Keys_path}/appcompany.json"
    try:
        with open(path_credentials, "w") as f:
            json.dump(user_credentials, f, indent=2)
    except:
        with open(path_credentials, "x") as f:
            json.dump(user_credentials, f, indent=2)

    firebase_keys = f'''
firebase_json_path="{path_credentials}"
firebase_db_url='{firebase_db_url}'
    '''

    with open(f"{Keys_path}/keys.env", "a") as f:
        f.write(firebase_keys)

    user_code_init_firebase = '''
from firebase_admin import initialize_app, credentials
import os
from dotenv import load_dotenv, find_dotenv

def init_firebase():
    dotenv_path= os.path.join(os.path.dirname(__file__), "keys.env")
    load_dotenv(dotenv_path=dotenv_path)
    firebase_json_path = os.getenv("firebase_json_path")
    firebase_db_url = os.getenv("firebase_db_url")
    cred = credentials.Certificate(firebase_json_path)
    app = initialize_app(cred, {
        'databaseURL': firebase_db_url
    })
    return app


    '''


    try:
        with open(f"{Keys_path}/fb.py", "w") as f:
            f.write(user_code_init_firebase)
    except:
        with open(f"{Keys_path}/fb.py", "x") as f:
            f.write(user_code_init_firebase)
