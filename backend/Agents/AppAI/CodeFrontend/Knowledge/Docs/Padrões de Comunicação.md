Padrões de Comunicação (Front-End)

1.1. Configuração de Requisições HTTP
ID: FRONT-API-COMMUNICATION
Palavras-Chave: front-end comunicação api axios fetch base url mock
Regra: O Front-End DEVE usar uma única instância de cliente HTTP configurada. Esta instância DEVE ser adaptável para chamar a API Real (usando BASE_URL) ou o Módulo de Mocking com base na variável de ambiente.

1.2. Tratamento de Erro na Comunicação (Front-End)
ID: FRONT-API-ERROR-HANDLE
Palavras-Chave: front-end tratamento erro 400 401
Regra: O Front-End DEVE capturar os status HTTP na camada de Hooks e reagir de acordo, utilizando o formato JSON de erro definido no Back-End (ID: CODE-API-ERROR-HANDLING).

Status Code	Ação Obrigatória do Front-End (Na camada de Hook/Context)
401 Unauthorized	Redirecionar o usuário para a página de Login.tsx e limpar o token localmente (no Context/Storage).
400 Bad Request	Retornar a mensagem de erro (campo message no JSON de erro) para a Page que irá exibir a mensagem no formulário.
404 Not Found	Exibir mensagem genérica de "Recurso não encontrado" ou redirecionar para uma página de erro 404.
1.3. Padrão de Autenticação (Token)
ID: FRONT-API-AUTH-TOKEN
Palavras-Chave: front-end autenticação token jwt bearer
Regra: Após o login, o token de acesso (JWT) DEVE ser armazenado em um local seguro (ex: localStorage ou sessionStorage com as devidas precauções) e enviado em TODAS as requisições subsequentes no cabeçalho Authorization: Bearer <token>.