Padrões de Código Essenciais (Flask e SQLAlchemy)

Esta documentação fornece o "como fazer" para o time de desenvolvimento, garantindo que os requisitos gerados pelo agente sejam implementados de forma consistente e com boas práticas básicas na stack Flask/PostgreSQL.

1. Padrão de Resposta e Erro da API (JSON)

1.1. Resposta de Sucesso Padrão

ID: CODE-API-SUCCESS
Palavras-Chave: flask resposta padrao json 200 201
Regra: Todas as respostas de sucesso DEVERÃO ser em formato JSON, encapsulando o objeto de dados.

Criação (POST): Usar status 201 Created.

Leitura/Atualização (GET/PUT): Usar status 200 OK.

Exemplo de Corpo de Resposta (200 OK):

{
  "status": "success",
  "message": "Operação realizada com sucesso.",
  "data": {
    "id": 101,
    "nome": "Usuário Teste",
    "email": "teste@exemplo.com"
  }
}


1.2. Tratamento de Erro Padrão

ID: CODE-API-ERROR-HANDLING
Palavras-Chave: flask tratamento erro 400 404 500
Regra: Em caso de erro, o status HTTP DEVE refletir a natureza do problema, e a resposta DEVE conter a chave "error".

Status Code

Causa Comum

Descrição para o Agente

400 Bad Request

Falha de validação de dados (ex: e-mail inválido, campo obrigatório faltando).

Gerar requisito para validar a entrada antes de chamar o Service.

401 Unauthorized

Token de acesso inválido ou ausente.

Gerar requisito para implementar um decorador de autenticação.

404 Not Found

Recurso não encontrado (ex: GET /usuarios/999 que não existe).

Gerar requisito para tratar o erro "Resource Not Found" no Service layer.

500 Internal Server Error

Erro inesperado no servidor.

Gerar requisito para um bloco try/except robusto na camada de Service.

2. Padrões CRUD com Flask-SQLAlchemy

2.1. Padrão de Leitura (Repository/Data Layer)

ID: CODE-DB-READ-GET
Palavras-Chave: sqlalchemy leitura find_by_id orm get
Regra: Usar session.get(Model, id) para buscar por chave primária.
Anti-Padrão a evitar: Nunca expor o objeto de banco de dados diretamente ao Controller. Sempre mapear para um DTO (Data Transfer Object) simples ou um dicionário.

2.2. Padrão de Criação e Commit

ID: CODE-DB-CREATE-COMMIT
Palavras-Chave: sqlalchemy criacao add commit
Regra: A criação de novos registros DEVE seguir o padrão novo_obj = Model(**dados); db.session.add(novo_obj); db.session.commit().

2.3. Padrão de Logs Assíncronos (MongoDB)

ID: CODE-DB-LOGS-MONGO
Palavras-Chave: mongodb logs assincronos
Regra: Logs de eventos não críticos (auditoria de acesso, erros não fatais) DEVERÃO ser enviados para o MongoDB. A chamada ao MongoDB deve ser non-blocking (se possível com thread ou pool), para não atrasar a resposta da API principal (PostgreSQL/Flask).

Exemplo de Estrutura de Log (MongoDB):

{
  "timestamp": "2025-10-07T10:00:00Z",
  "user_id": 101,
  "action": "LOGIN_SUCCESS",
  "ip_address": "192.168.1.1",
  "details": {
    "device": "Mobile",
    "browser": "Chrome"
  }
}


3. Segurança Essencial para Juniores

3.1. Validação de Entrada de Dados (Input Validation)

ID: SEC-INPUT-VALIDATION
Palavras-Chave: segurança validacao pydantic
Regra: Toda entrada de dados (corpo da requisição, parâmetros de query) DEVE ser validada imediatamente no Controller/View com uma biblioteca como o Pydantic ou similar antes de chegar na camada de Service. Isso previne injeções e garante a integridade dos tipos de dados.

3.2. Senhas Seguras (Hashing)

ID: SEC-PASSWORD-HASH
Palavras-Chave: segurança hash de senha bcrypt
Regra: Senhas DEVERÃO ser armazenadas com hashing forte. O uso de Bcrypt é obrigatório. NUNCA armazenar senhas em texto puro ou com hash MD5/SHA-1. A verificação da senha deve ser feita pelo hash