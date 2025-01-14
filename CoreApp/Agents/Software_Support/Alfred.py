

#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp.SoftwareAI.Instructions._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp.SoftwareAI.Tools._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################



class AlfredSupport_Mullvadvpn_auto_rotate:
    def __init__(self, appfb, client):
        self.appfb = appfb
        self.client = client
        self.TOKEN =  '6960196439:AAH_iy8c3pm-MHUUciVyvxBf7OvxgcMUJ2M'
        self.CHANNEL_ID = '6960196439'
        self.user_threads = {}
        self.emojis = ['😊', '🤖', '🚀', '💡', '🎉']


        self.tools_Alfred = None
        self.adxitional_instructions_Alfred = ""
        self.key = "AI_Tigrao_Escritor_de_documento_Pre_Projeto"
        self.nameassistant = "AI Tigrao Escritor de documento Pre-Projeto"
        self.model_select = "gpt-4o-mini-2024-07-18"
        self.Upload_1_file_in_thread = None
        self.Upload_1_file_in_message = None
        self.Upload_1_image_for_vision_in_thread = None
        self.Upload_list_for_code_interpreter_in_thread = None
        self.vectorstore_in_Thread = None
        self.vectorstore_in_agent = None


    def Alfred(self, mensagem, user_id):


        AI_Tigrao, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(self.appfb, self.client, key, instructionTigrao, nameassistant, model_select, tools_Tigrao, vectorstore_in_agent)
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensagem,
                                                                agent_id=AI_Tigrao, 
                                                                key=self.key,
                                                                user_id=user_id,
                                                                app1=self.appfb,
                                                                client=self.client,
                                                                tools=self.tools_Alfred,
                                                                model_select=self.model_select,
                                                                aditional_instructions=self.adxitional_instructions_Alfred
                                                                )
                                                
                 
        ##Agent Destilation##                   
        Agent_destilation.DestilationResponseAgent(mensage3, response, instructionsassistant, nameassistant)
        
        path_name_doc_Pre_Projeto = os.getenv("PATH_NAME_DOC_PRE_PROJETO_ENV")
        return path_name_doc_Pre_Projeto



    def handle_save_ticket(self, order_id, nvar_key, issue_description):
        ticket_id = self.save_support_ticket(order_id, nvar_key, issue_description)
        return {"ticket_id": ticket_id.key}

    def callable_save_support_ticket(self, order_id, nvar_key, issue_description):
        return self.save_support_ticket(order_id, nvar_key, issue_description)

    def enviar_resposta_com_emoji(self, resposta):
        emoji = random.choice(self.emojis)
        resposta_com_emoji = f"{emoji} {resposta}"
        return resposta_com_emoji

    def start(self, update, context):
        user_id = update.message.from_user.id
        if user_id not in self.user_threads:
            self.user_threads[user_id] = self.client.beta.threads.create()
        update.message.reply_text('Olá! Como posso ajudar você hoje?')

    def reply_message(self, update, context):
        user_message = update.message.text
        user_id = update.message.from_user.id
        
        if user_id not in self.user_threads:
            self.user_threads[user_id] = self.client.beta.threads.create()
            
        thread_id = self.user_threads[user_id]
        print(user_message)
        Alfred_response = self.Alfred(user_message, user_id)
        update.message.reply_text(Alfred_response)

    def save_support_ticket(self, order_id, nvar_key, issue_description):
        ref = db.reference('support_ticket', app=app1)
        ticket_id = ref.push({
            'order_id': order_id,
            'mvar_key': nvar_key,
            'issue_description': issue_description,
            'timestamp': datetime.now().isoformat()
        })
        print(f"Ticket saved with ID: {ticket_id.key}")
        return ticket_id.key 




    def main():
        updater = Updater(TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_message))

        updater.start_polling()
        updater.idle()

