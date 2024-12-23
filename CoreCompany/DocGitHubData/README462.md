
# Documentação do Software

## 🌟 Introdução
Bem-vindo à documentação do nosso software! 🎉 Este projeto consiste em uma aplicação Flask que permite a criação de landing pages personalizadas.

### Visão geral do projeto
O objetivo principal deste software é permitir que os usuários gerem landing pages ao fornecer um título, conteúdo e uma imagem.

### Propósito principal
Facilitar a criação de landing pages de forma intuitiva e organizada.

### Funcionalidades-chave
- Formulário de entrada para título, conteúdo e imagem.
- Validação de dados do formulário.
- Upload seguro de imagens.

## ⚙️ Instalação
Para instalar e rodar esta aplicação, siga os passos abaixo! 🚀

### Requisitos do sistema
- Python 3.x
- Flask
- Flask-WTF
- WTForms

### Dependências necessárias
Instale as dependências com o seguinte comando:
```bash
pip install Flask Flask-WTF WTForms
```

### Guia passo-a-passo
1. Clone o repositório do projeto:
   ```bash
   git clone <URL_DO_REPOSITORIO>
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd <NOME_DA_PASTA>
   ```

### Configuração inicial
Antes de executar a aplicação, certifique-se de que a pasta `uploads/` existe. O código já verifica e cria essa pasta ao iniciar a aplicação.

## 🎮 Uso
A aplicação é bastante fácil de usar! 🥳

### Exemplos práticos
1. Inicie a aplicação:
   ```bash
   python app.py
   ```
2. Acesse a aplicação em seu navegador no endereço: `http://127.0.0.1:5000/`

### Comandos principais
Use o formulário na página inicial para adicionar um título, conteúdo e uma imagem. Após o envio, você será redirecionado para a landing page gerada.

### Configurações disponíveis
Configure o `SECRET_KEY` no `app.config` para uma melhor segurança.

### Casos de uso comuns
- Criação de landing pages para promoções.
- Portfólios pessoais.
- Páginas de captura para eventos.

## 🔌 API
Este software não possui uma API RESTful no momento, mas as rotas principais são:

### Endpoints disponíveis
- `GET /` - Renderiza a página inicial com o formulário.
- `POST /` - Envia os dados do formulário e gera a landing page.

### Métodos e parâmetros
- Para `POST /`:
  - `title`: Título da landing page.
  - `content`: Conteúdo da landing page.
  - `image`: Imagem a ser carregada.

### Exemplos de requisições
- Você pode testar a funcionalidade enviando um formulário na interface.

### Respostas esperadas
A aplicação redirecionará para a página da landing page com os dados que você forneceu.

## 🤝 Contribuição
Contribuições são bem-vindas! 💖 Veja abaixo como você pode contribuir.

### Guia para contribuidores
1. Faça um fork deste repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`).
3. Faça suas alterações e commit (`git commit -m 'Adiciona nova funcionalidade'`).
4. Envie para o repositório original (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

### Padrões de código
Siga as melhores práticas de codificação em Python e utilize o PEP 8 como guia.

### Processo de Pull Request
- As alterações devem ser revisadas antes de serem mescladas à branch principal.

### Boas práticas
- Sempre escreva testes para novas funcionalidades.

## 📜 Licença
Este projeto está sob a licença MIT. 📄

### Tipo de licença
MIT License

### Termos de uso
Você é livre para usar, modificar e distribuir o software, desde que mantenha os avisos de direitos autorais.

### Restrições
Não assuma a propriedade intelectual e não utilize este software para fins ilícitos.

---

Esta documentação deve fornecer uma base sólida para qualquer novo desenvolvedor ou usuário que deseje entender e utilizar o software! 😊