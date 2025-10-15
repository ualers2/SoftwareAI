0. Padrões de Arquitetura Simplificada
Arquitetura Padrão: Monolito Simples (MVC/Camadas)
ID: ARQ-MONOLITO-SIMPLES
Palavras-Chave: arquitetura monolito simples mvc camadas
Padrão: Adotar o padrão de Camadas (Presentation -> Service -> Data/Repository) ou MVC (Model-View-Controller) para organizar o código.
Fluxo: O Flask (Presentation/Controller) chama a camada de Serviço (Service) para executar a lógica de negócio, que, por sua vez, usa a camada de Repositório (Data/Repository) para interagir com o PostgreSQL.
Vantagem: É fácil de navegar, testar e é a arquitetura inicial mais recomendada para aprender a base.

Padrões de Convenção e Estrutura de Código (Back-End)
Este documento mapeia a estrutura de pastas do Back-End para as responsabilidades do código, garantindo que o time júnior saiba onde colocar cada tipo de lógica.

1. Mapeamento da Estrutura de Módulos (Separation of Concerns)
A estrutura de Back-End/Modules implementa o padrão de Camadas de Serviço (Service Layer), separando as preocupações:

Pasta

Responsabilidade

Descrição

Padrões de Uso (ID RAG)

Routes

Interface (Controller)

Contém os arquivos auth.py, user.py, etc., que definem as rotas (URL, métodos HTTP). A única responsabilidade é receber a requisição, validar a entrada (Pydantic), e chamar a camada de Service (Resolvers). NUNCA deve conter lógica de negócio ou acesso direto ao banco.

STACK-BACK-FLASK, CODE-API-SUCCESS

Resolvers

Lógica de Negócio (Service)

O coração da aplicação. Contém a lógica de negócio principal (ex: user_register.py, generate_invoice_pdf.py). Recebe dados validados da Routes, executa a regra de negócio e coordena chamadas a Geters, Savers e Helpers.

ARQ-BUSINESS-SERVICE, CODE-API-ERROR-HANDLING

Geters

Acesso à Leitura (Repository)

Funções puras para ler dados de PostgreSQL (via Flask-SQLAlchemy) ou MongoDB (logs/auditoria). Ex: get_user_by_email().

STACK-DB-POSTGRES, CODE-DB-READ-GET

Savers

Acesso à Escrita (Repository)

Funções puras para escrever ou atualizar dados no PostgreSQL ou MongoDB. Ex: create_new_user(), log_action(). Contém o db.session.commit().

STACK-DB-POSTGRES, STACK-DB-MONGO-LOGS, CODE-DB-CREATE-COMMIT

Helpers

Funções Utilitárias

Código sem estado, reutilizável, que não contém lógica de negócio ou acesso ao banco. Ex: format_date(), validate_cpf(), calculate_discount().

-

Config

Configuração da Aplicação

Inicialização de módulos (Flask, SQLAlchemy, MongoDB, etc.) e carregamento de variáveis de ambiente.

-

2. Convenções de Nomenclatura e Arquivos
2.1. Nomenclatura de Arquivos
ID: CONV-FILE-NAMING
Regra: Usar snake_case para todos os nomes de arquivos Python e pastas, sendo descritivo.

Bom: user_registration_resolver.py, get_all_products.py

Ruim: UserRegistration.py, Getallproducts.py

2.2. Nomenclatura de Funções
ID: CONV-FUNC-NAMING
Regra: Funções devem usar verbos no infinitivo para indicar a ação que realizam (ex: get, create, update, send, generate).

Funções em Resolvers: Devem descrever o processo: register_new_user(), process_order().

Funções em Geters/Savers: Devem ser diretas ao DB: get_user_by_id(), save_new_log().

2.3. Uso de try...except
ID: CONV-TRY-EXCEPT
Regra: O bloco try...except DEVE ser usado primariamente na camada Resolvers (Service) e NÃO nas rotas. As rotas devem apenas capturar a exceção tratada e mapear para a resposta HTTP (ex: 400 Bad Request).

Anti-Padrão:

# Módulos/Routes/user.py (ANTI-PADRÃO)
@user_bp.route('/register', methods=['POST'])
def register():
    try:
        # Lógica de negócio ou DB aqui
        ...
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
3. arquitetura desejavel:
```
nomedoprojeto\
├── Readme.md
├── docker-compose.yml
└── .github\
    └── workflows\
        ├── deploy.yml
└── Front-End\
    └── vite.config.ts
    └── tsconfig.node.json
    └── tsconfig.json
    └── tsconfig.app.json
    └── tailwind.config.ts
    └── postcss.config.js
    └── package.json
    └── Dockerfile
    └── package-lock.json
    └── index.html
    └── eslint.config.js
    └── components.json
    └── .env
    └── public\
    └── src\
      └── components\
          ├── ...
      └── constants\
          ├── ...
      └── contexts\
          ├── ...
      └── hooks\
          ├── ...
      └── lib\
          ├── ...
      └── pages\
          ├── Login.tsx
          ├── ...
      └── App.css
      └── App.tsx
      └── index.css
      └── main.tsx
      └── vite-env.d.ts
      
└── Back-End\
    ├── requirements.txt
    ├── Dockerfile
    ├── api.py
    └── Keys\
        ├── keys.env
    └── Models\
        └── mongoDB\
            ├── audit.py
            ├── logs.py
        └── postgreSQL\
            ├── user.py
            ├── ...
    └── Modules\
        └── Config\
            ├── setup.py
            ├── ...
        └── Geters\
            ├── logs.py
            ├── user_by_access_token.py
            ├── user_by_email.py
            ├── ...
        └── Helpers\
            ├── ...
        └── Resolvers\
            ├── generate_invoice_pdf.py
            ├── send_email.py
            ├── user_identifier.py
            ├── ...
        └── Routes\
            ├── auth.py
            ├── ...
        └── Savers\
            ├── log_action.py
            ├── log_audit.py
            ├── log_system_health.py
            ├── ...
        └── Updaters\
            ├── ...
      
```
