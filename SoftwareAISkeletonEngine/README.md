 # SoftwareAI Skeleton Engine

 **Economize até 10x em tokens criando esqueletos prontos de projetos**

 Esqueletos funcionais com backend e suporte a Docker.

 ## Esqueletos Disponíveis

 - **flask-web-product**: Esqueleto pronto para receber um SaaS com integração de pagamento via Stripe.

 ## Quickstart

 ### Pré-requisitos
 - Node.js (v14+)
 - NPM ou Yarn
 - (Opcional) Docker e Docker Compose, se desejar executar em containers

 ### Instalação
 Instalação global via NPM:
 ```bash
 npm install -g softwareai-skeleton-engine
 ```
 Ou via Yarn:
 ```bash
 yarn global add softwareai-skeleton-engine
 ```

 ### Criando um novo projeto
 Após a instalação, use o comando abaixo para criar seu projeto:
 ```bash
 # Usando o comando global
 create-py-app meu-projeto --theme flask-web-product

 # Ou sem instalar globalmente (via npx)
 npx create-py-app meu-projeto --theme flask-web-product
 ```
 Se nenhum tema for informado, o padrão `flask-web-product` será utilizado.

 ### Executando o projeto
 1. Acesse o diretório do projeto:
    ```bash
    cd meu-projeto
    ```
 2. (Opcional) Crie e ative um ambiente virtual Python:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
 3. Instale as dependências Python:
    ```bash
    pip install -r requirements.txt
    ```
 4. Execute a aplicação:
    - Diretamente com Python:
      ```bash
      python app.py
      ```
    - Ou usando Docker Compose:
      ```bash
      python build.py
      ```
 5. Acesse em `http://localhost:5000`

 ## Contribuição
 1. Faça um fork deste repositório
 2. Crie uma branch para sua feature (`git checkout -b feature/minha-feature`)
 3. Faça suas alterações e commit (`git commit -am 'Adiciona feature X'`)
 4. Envie para o seu repositório (`git push origin feature/minha-feature`)
 5. Abra um Pull Request

 ## Licença
 Este projeto está licenciado sob a licença MIT.









