2. Padrões de Testes Unitários (Back-End Python)

Garantir que os juniores saibam como testar as camadas separadas é o maior impulsionador de qualidade em um projeto monolítico.

2.1. Ferramenta de Teste

ID: TEST-PY-TOOL
Palavras-Chave: testes python unitarios pytest
Regra: Utilizar o pytest como framework de testes unitários padrão.

2.2. Testes para a Camada de Serviço (Resolvers)

ID: TEST-PY-RESOLVER-MOCK
Palavras-Chave: testes resolvers service mocking
Regra: Ao testar um arquivo em Modules/Resolvers/, é OBRIGATÓRIO utilizar mocking para simular as respostas das funções de acesso ao banco de dados (Geters e Savers). O teste deve verificar apenas a lógica de negócio (ex: o cálculo, a validação de regras).

Exemplo: Para testar Resolvers/process_order.py, o teste deve simular que Savers/save_order.py retornou sucesso, sem tocar no PostgreSQL.

2.3. Testes para as Camadas de Dados (Geters/Savers)

ID: TEST-PY-DB-INTEGRATION
Palavras-Chave: testes geters savers banco dados integration
Regra: Testes de Geters e Savers devem ser considerados testes de integração (unitários) e DEVERIAM (se possível no ambiente de CI/CD) rodar contra um banco de dados temporário ou em memória para garantir que as queries SQL/ORM estão corretas.

Alternativa Simples: Para juniores, o teste mais básico é garantir que, ao chamar a função Savers/save_order(), o objeto correto do ORM é criado e a sessão é chamada para adição.

2.4. Localização dos Testes

ID: TEST-PY-LOCATION
Regra: Todos os arquivos de teste devem residir em uma pasta separada (ex: Back-End/tests/) e ter o prefixo test_ no nome (ex: test_user_resolver.py).