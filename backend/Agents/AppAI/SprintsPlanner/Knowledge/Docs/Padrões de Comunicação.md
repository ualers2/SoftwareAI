1. Padrão de Comunicação (Front-End)

1.1. Configuração de Requisições HTTP

ID: FRONT-API-COMMUNICATION
Palavras-Chave: front-end comunicação api axios fetch base url
Regra: O Front-End DEVE usar uma única instância de cliente HTTP (como Axios ou Fetch API) configurada com uma BASE_URL (lida do .env do Front-End) e com o cabeçalho Content-Type: application/json padrão.

1.2. Tratamento de Erro na Comunicação (Front-End)

ID: FRONT-API-ERROR-HANDLE
Palavras-Chave: front-end tratamento erro 400 401
Regra: O Front-End DEVE capturar os status HTTP e reagir de acordo, utilizando o formato JSON de erro definido no Back-End (CODE-API-ERROR-HANDLING).

Status Code

Ação Obrigatória do Front-End

401 Unauthorized

Redirecionar o usuário para a página de Login.tsx e limpar o token localmente.

400 Bad Request

Exibir a mensagem de erro (campo message no JSON de erro) diretamente no formulário, de forma amigável ao usuário.

404 Not Found

Exibir mensagem genérica de "Recurso não encontrado" ou redirecionar para uma página de erro 404.

1.3. Padrão de Autenticação (Token)

ID: FRONT-API-AUTH-TOKEN
Palavras-Chave: front-end autenticação token jwt bearer
Regra: Após o login, o token de acesso (JWT) DEVE ser armazenado em um local seguro (ex: localStorage ou sessionStorage com as devidas precauções) e enviado em TODAS as requisições subsequentes no cabeçalho Authorization: Bearer <token>.