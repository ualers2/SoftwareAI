#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################


def AutoGetLoggerUser(appcompany, appproduct, ticketid):
        
    support_ticket = db.reference(f'support_ticket/{ticketid}', app=appcompany)
    data1 = support_ticket.get()

    issue_description_db = data1['issue_description']
    timestamp_open_db = data1['timestamp_open']
    user_email_db = data1['user_email']

    user_email_db_str = f"{user_email_db}"
    user_email_replace = user_email_db_str.replace("@gmail.com", "")
    data = datetime.fromisoformat(timestamp_open_db)

    # 1 day interval before timestamp_open_db
    data_inicial = data - timedelta(days=1)
    datas_intervalo = [(data_inicial + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6)]

    logger_data_combined = {}

    for data_format in datas_intervalo:
        Logger_support_ticket = db.reference(f'Logger/User_{user_email_replace}/{data_format}', app=appproduct)
        data_Logger = Logger_support_ticket.get()
        if data_Logger:
            logger_data_combined[data_format] = data_Logger

    return issue_description_db, logger_data_combined
