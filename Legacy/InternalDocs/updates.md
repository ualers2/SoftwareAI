

## 13/04/2025

- [X] ``/api/response-conversation`` adicionado a funcao autenticar_usuario usando a api key fornecida, @limiter.limit(dynamic_rate_limit)  adicionado para evitar spam e controlar o limite de cada plano
- [X] ``/api/response-conversation/documentation-architect-agent`` adicionado a funcao autenticar_usuario usando a api key fornecida, @limiter.limit(dynamic_rate_limit)  adicionado para evitar spam e controlar o limite de cada plano

## 14/04/2025

- [X] ``/webhook`` ajustado para enviar WEBHOOK_SECRET_flag para ``/api/register`` que é o WEBHOOK_SECRET da aplicacao, ajustado para aceitar o upgrade da conta com status code de 409 enviando ao email do usuario seu upgrade, mensagem de upgrade de conta melhor

- [X] ``/api/response-conversation`` utilizando dynamic_rate_limit que busca o limit em users/{email} do usuario definido por ``/api/register``
- [X] ``/api/response-conversation/documentation-architect-agent`` utilizando dynamic_rate_limit que busca o limit em users/{email} do usuario definido por ``/api/register``
- [X] ``/api/response-conversation/documentation-architect-agent`` utilizando a nova ferramenta autobuildpdf que de





