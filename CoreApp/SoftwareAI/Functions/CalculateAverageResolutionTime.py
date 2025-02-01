def CalculateAverageResolutionTime():
    ref = db.reference('support_ticket', app=appfb)
    tickets = ref.get()

    if not tickets:
        return "Nenhum ticket encontrado."

    resolution_times = [
        ticket.get('resolution_time_minutes', 0)
        for ticket in tickets.values()
        if ticket.get('status') == 'close'
    ]

    if not resolution_times:
        return "Nenhum ticket fechado encontrado."

    average_resolution_time = sum(resolution_times) / len(resolution_times)
    return f"Tempo Médio de Resolução: {average_resolution_time:.2f} minutos"
