

# 📖 Criando uma pipiline com o agente
- primeiro, abra as`` configuracoes -> Webhook ``
- aponte o Payload URL para a url efemera do conteiner do agente 
- em Content type defina para ``application/json``
- configure sua Secret (salve para usar no env)
- selecione ``Let me select individual events.``
- em trigger do webhook precisamos somente dos eventos Issues e Issue comments
- pronto click em add webhook
- abra keys.env defina GITHUB_WEBHOOK_SECRET como sua Secret
