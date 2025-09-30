
        
        


import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import os

diretorio_script = os.path.dirname(os.path.abspath(__file__))
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
os.makedirs(os.path.join(diretorio_script, "../", '../', 'Logs'), exist_ok=True)
file_handler = logging.FileHandler(os.path.join(diretorio_script, '../',"../", 'Logs', 'send_email.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__),
    "../",
    "../",
    "Keys", 
    "keys.env"
    ))

def SendEmail(
    user_email_origin="",
    html_attach_flag=True,
    email_type="Failed Project",

    SMTP_ADM="",
    SMTP_PASSWORD="",
    SMTP_HOST="",
    SMTP_PORT="",
    use_tls="",

    erro_project="",
    title_origin="",
    new_scheduled_time="",
    planname=''
    ):
    """
    email_type: "Sucess Upgrated Account", "Failed Project", "Sucess Project", "Server Limitation", "Tiktok Publish Fail", "Youtube Publish Fail", "Sucess Created Account"
    """    
    template_path = os.path.join(diretorio_script, '../', '../', "EmailTemplates")
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as SMTP_server:
        SMTP_server.connect(SMTP_HOST, SMTP_PORT)
        if use_tls:
            SMTP_server.starttls()
        SMTP_server.login(SMTP_ADM, SMTP_PASSWORD)
        MIME_server = MIMEMultipart()
        MIME_server['From'] = f"Media Cuts Studio <{SMTP_ADM}>"
        MIME_server['To'] = user_email_origin
        try:    
            if email_type == "Failed Project":
                corpo = f"""
                Olá Nao foi possivel executar seu projeto com maestria pedimos desculpas e a compreencao que é natural que ocorra erros na versao beta 
                enviaremos o seguinte erro para os desenvolvedores: \n {erro_project} \n
                """
                MIME_server['Subject'] = "O projeto falhou"
                html_body = open(os.path.join(template_path, "FalhaDeProjeto.html"), encoding='utf-8').read().replace("{{erro}}", str(erro_project))

            elif email_type == "Sucess Project":
                corpo = f"""
                Olá viemos informar que seu projeto\n
                {title_origin}\n
                foi executado com maestria confira no seu painel de projetos localizado em\n
                https://mediacutsstudio.com/projects
                """
                MIME_server['Subject'] = "O projeto foi um sucesso"
                html_body =  open(os.path.join(template_path, "SucessoDeProjeto.html"), encoding='utf-8').read().replace("{{title_origin}}", str(title_origin))

            elif email_type == "Server Limitation":
                corpo = f"""
                Olá Nao foi possivel colocar seu projeto {title_origin} em execucao por conta da limitacao do servidor\n
                Mas nao se preocupe agendamos a execucao do seu projeto para o seguinte horario: \n
                {new_scheduled_time}
                """
                MIME_server['Subject'] = "Limitacao do servidor"
                html_body =  open(os.path.join(template_path, "server_limit.html"), encoding='utf-8').read().replace("{{title}}", title_origin).replace("{{new_scheduled_time}}", new_scheduled_time)

            elif email_type == "Tiktok Publish Fail":
                corpo = f"""
                Olá Nao foi possivel enviar o video vertical {title_origin} para o tiktok\n
                o seguinte erro aconteceu: \n {erro_project} \n
                """
                MIME_server['Subject'] = "Nao foi possivel enviar o Tiktok"
                html_body =  open(os.path.join(template_path, "email_tiktok_fail.html"), encoding='utf-8').read().replace("{{title}}", title_origin).replace("{{errupload1}}", str(erro_project))

            elif email_type == "Youtube Publish Fail":
                corpo = f"""
                Olá Nao foi possivel enviar o shorts {title_origin} para o youtube\n
                o seguinte erro aconteceu: \n
                {erro_project}
                """
                MIME_server['Subject'] = "Nao foi possivel enviar o Youtube"
                html_body =  open(os.path.join(template_path, "email_youtube_fail.html"), encoding='utf-8').read().replace("{{title}}", title_origin).replace("{{error_content}}", str(erro_project))

            elif email_type == "Sucess Created Account":
                corpo = f"""
                🎉 Bem-vindo(a) ao Media Cuts Studio!
                Olá {user_email_origin}, sua conta foi criada com sucesso.
                Agora você já pode acessar o painel e começar a criar seus projetos de cortes automáticos!
                https://mediacutsstudio.com/login
                Media Cuts Studio © 2025
                
                """
                MIME_server['Subject'] = "Conta criada com sucesso - Media Cuts Studio"
                html_body =  open(os.path.join(template_path, "email_account_success.html"), encoding='utf-8').read().replace("{{username}}", user_email_origin)

            elif email_type == "Sucess Upgrated Account":
                corpo = f"""
                🎉 Bem-vindo(a) ao Media Cuts Studio!
                Olá {user_email_origin}, sua conta foi atualizada com sucesso.
                Agora você já pode acessar o painel e começar a criar seus projetos de cortes automáticos!
                https://mediacutsstudio.com/login
                Media Cuts Studio © 2025
                
                """
                MIME_server['Subject'] = f"Seu conta foi atualizada para o Plano {planname} 🚀"
                html_body =  open(os.path.join(template_path, "email_plan_upgraded.html"), encoding='utf-8').read().replace("{{username}}", user_email_origin)

            if html_attach_flag == True:
                MIME_server.attach(MIMEText(html_body, "html"))
            elif html_attach_flag == False:
                MIME_server.attach(MIMEText(corpo, "plain"))

            SMTP_server.sendmail(SMTP_ADM, user_email_origin, MIME_server.as_string()) 
            logger.info(f"Email '{email_type}' enviado com sucesso!")
            SMTP_server.quit()
        except Exception as eerrorsendemail:
            logger.warning(f"erro ao enviar o email de sinalizacao de erro {eerrorsendemail}")



# if __name__ == '__main__':

#     host = os.getenv('SMTP_HOST')
#     port = int(os.getenv('SMTP_PORT', 587))
#     SMTP_USER = os.getenv('SMTP_USER')
#     password = os.getenv('SMTP_PASSWORD')
#     use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
#     user_email_origin = "freitasalexandre810@gmail.com"
#     erro_project = "erro de teste"
#     title_origin = "projeto de teste"
#     new_scheduled_time = "2025-08-05 21:42:04"


#     SendEmail(
#         user_email_origin=user_email_origin,
#         html_attach_flag=True,
#         email_type="Sucess Created Account",
        
#         SMTP_ADM=SMTP_USER,
#         SMTP_PASSWORD=password,
#         SMTP_HOST=host,
#         SMTP_PORT=port,
#         use_tls=use_tls,


#         erro_project=erro_project,
#         title_origin=title_origin,
#         new_scheduled_time=new_scheduled_time
#     )
