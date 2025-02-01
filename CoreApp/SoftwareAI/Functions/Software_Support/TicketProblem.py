#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################



def OpenSupportTicketProblem(appfb, user_email, issue_description):
    full_hash = hashlib.sha256(issue_description.encode('utf-8')).hexdigest()
    ticketid = full_hash[:5]
    ref = db.reference('support_ticket', app=appfb)
    ticketdatasetkey = ticketid
    ticketdataset = {
        'user_email': user_email,
        'issue_description': issue_description,
        'timestamp_open': datetime.now().isoformat(),
        'status': "open",
        'ticketid': ticketid,
        'csat': "None"  # Inicialmente sem feedback
    }
    ref.child(ticketdatasetkey).set(ticketdataset)
    return f"Open Ticket ID: {ticketid}"

def CloseSupportTicketProblem(appfb, ticketid):
    ref = db.reference(f'support_ticket/{ticketid}', app=appfb)
    data = ref.get()
    
    if not data:
        return f"Ticket ID {ticketid} not found."

    data['timestamp_close'] = datetime.now().isoformat()
    data['status'] = "closed"
    ref.set(data)
    return f"Closed Ticket ID: {ticketid}"

def RecordCSAT(appfb, ticketid, csat_score):
    ref = db.reference(f'support_ticket/{ticketid}', app=appfb)
    data = ref.get()

    if not data:
        return f"Ticket ID {ticketid} not found."

    data['csat'] = csat_score
    ref.set(data)
    return f"CSAT registrado para o Ticket ID: {ticketid}"
