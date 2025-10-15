1. Stack Tecnológica Padrão e Justificativas
1.1. Backend para Início Rápido e Clareza
ID: STACK-BACK-FLASK
Palavras-Chave: stack backend python flask blueprint api
Decisão: Python com framework Flask.
Justificativa (Simplicidade): Flask é um micro-framework com pouca "magia" (convenções), permitindo que o desenvolvedor júnior entenda o fluxo de requisição e resposta rapidamente.
Estrutura de API: Utilizar Flask Blueprints para organizar a API por módulos (ex: blueprint_usuarios, blueprint_produtos), mantendo o código limpo e o roteamento claro.

1.2. Banco de Dados Relacional (Transacional)
ID: STACK-DB-POSTGRES
Palavras-Chave: stack db postgresql flask_sqlalchemy dados transacionais
Decisão: PostgreSQL com ORM Flask-SQLAlchemy.
Justificativa (ACID): PostgreSQL é robusto e gratuito, garantindo integridade e atomicidade dos dados transacionais (pedidos, perfis, etc.).
Justificativa (ORM): O Flask-SQLAlchemy abstrai a complexidade do SQL, permitindo que juniores interajam com o banco de dados usando objetos Python (Modelos), o que acelera o desenvolvimento e reduz erros de SQL.

1.3. Banco de Dados Não Relacional (Logs e Eventos)
ID: STACK-DB-MONGO-LOGS
Palavras-Chave: stack db mongodb logs auditoria eventos
Decisão: MongoDB para armazenamento de Logs, Auditoria e Eventos não estruturados.
Justificativa (Flexibilidade): Documentos JSON (BSON) são ideais para logs, pois o schema de um log pode mudar sem afetar a aplicação principal. Não é necessário definir schemas complexos para dados não críticos.
Regra de Ouro: NUNCA armazenar dados transacionais ou críticos para o negócio no MongoDB.