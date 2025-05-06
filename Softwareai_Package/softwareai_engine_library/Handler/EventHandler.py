
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
# IMPORT SoftwareAI Core
from softwareai_engine_library.Inicializer._init_core_ import *
#########################################
import re
from pydantic import BaseModel
from firebase_admin import App
import importlib

class EventHandler(AssistantEventHandler):
    def __init__(self, 
                OPENAI_API_KEY,
                Debug, 
                lang, 
                app_product,
                threead_id,
                client,
                app1,
                 
            ):
        self.Debug = Debug
        self.lang = lang
        self.app_product = app_product
        self.threead_id = threead_id
        self.client = client
        self.app1 = app1
        self.OPENAI_API_KEY = OPENAI_API_KEY

    def list_runs(self, api_key, thread_id, after=None, before=None, limit=20, order="desc"):
        url = f"https://api.openai.com/v1/threads/{thread_id}/runs"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "OpenAI-Beta": "assistants=v2"
        }
        params = {
            "after": after,
            "before": before,
            "limit": limit,
            "order": order
        }
        # Remove parâmetros que são None
        params = {k: v for k, v in params.items() if v is not None}
        
        response = requests.get(url, headers=headers, params=params)
        return response.json()

    @override
    def on_text_created(self, text: Text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta: TextDelta, snapshot: Text):
        print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call: ToolCall):
        print(f"\nassistant > a {tool_call.type}\n", flush=True)

        if tool_call.type == 'function':
            function_name = tool_call.function.name
            function_arguments = tool_call.function.arguments

        
            self.log_message(f'🔧 Função chamada: {function_name}',
                        f'🔧 Function called: {function_name}', 'yellow')
            self.log_message(f'📥 Argumentos: {function_arguments}',
                        f'📥 Arguments: {function_arguments}', 'yellow')
            self.log_message(f'🆔 Tool Call ID: {tool_call.id}',
                        f'🆔 Tool Call ID: {tool_call.id}', 'yellow')

            THREAD_ID = "thread_Md0Dnjy6Q49fHOKrtsDsReWd"

            result = self.list_runs(self.OPENAI_API_KEY, THREAD_ID)

            last_id = result["last_id"]

            # if self.app_product:
            #     _init_output_(
            #         function_name,
            #         function_arguments,
            #         tool_call,
            #         self.threead_id,
            #         self.client,
            #         last_id,
            #         self.app1,
            #         OpenAIKeysinit,
            #         OpenAIKeysteste,
            #         GithubKeys,
            #         python_functions,
            #         Agent_files_update,
            #         AutenticateAgent,
            #         ResponseAgent,
            #         self.app_product,
            #     )
            # else:
            #     _init_output_(
            #         function_name,
            #         function_arguments,
            #         tool_call,
            #         self.threead_id,
            #         self.client,
            #         last_id,
            #         self.app1,
            #         OpenAIKeysinit,
            #         OpenAIKeysteste,
            #         GithubKeys,
            #         python_functions,
            #         Agent_files_update,
            #         AutenticateAgent,
            #         ResponseAgent,
            #     )


    def log_message(self, message_pt, message_en, color, bold=False):
        if self.Debug:
            attrs = ['bold'] if bold else []
            cprint(message_pt if self.lang == "pt" else message_en, color, attrs=attrs)

    @override
    def on_tool_call_delta(self, delta: ToolCallDelta, snapshot: ToolCall):
        if delta.type == "code_interpreter" and delta.code_interpreter:
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
