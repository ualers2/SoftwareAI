def CalculateAverageCSAT(testeid, appfb):
    ref = db.reference('support_ticket', app=appfb)
    tickets = ref.get()

    if not tickets:
        return "Nenhum ticket encontrado."

    csat_scores = [ticket['csat'] for ticket in tickets.values() if ticket['csat'] is not None]
    
    if not csat_scores:
        return "Nenhum feedback de CSAT registrado ainda."

    avg_csat = sum(csat_scores) / len(csat_scores)
    return f"Pontuação média de satisfação (CSAT): {avg_csat:.2f}"
