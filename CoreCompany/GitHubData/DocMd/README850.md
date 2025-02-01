
# Gerador de Nomes de Cursos

## Introdução
Este é um aplicativo web simples construído com Flask e NLTK, destinado a gerar sugestões de nomes para cursos com base em um tema ou descrição fornecido pelo usuário. O aplicativo utiliza técnicas de processamento de linguagem natural para tokenizar a entrada e gerar nomes criativos.

## Instalação

Para instalar e rodar este software, siga os passos abaixo:

### Pré-requisitos
- Python 3.x
- pip (gerenciador de pacotes do Python)
- NLTK (Natural Language Toolkit)

### Passos de Instalação

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/seu_usuario/gerador-nomes-cursos.git
   cd gerador-nomes-cursos
   ```

2. **Instale as dependências:**
   ```bash
   pip install Flask nltk
   ```

3. **Baixar recursos necessários do NLTK:**
   Caso execute o aplicativo pela primeira vez, você precisa descomentar a linha de download no código:
   ```python
   # nltk.download('punkt') # Descomente esta linha se executar pela primeira vez
   ```

4. **Execute o aplicativo:**
   ```bash
   python app.py
   ```

5. **Acesse o aplicativo:**
   Abra o seu navegador e acesse `http://127.0.0.1:5000/`

## Uso
Para gerar sugestões de nomes de cursos, siga os passos abaixo:

1. No formulário na página inicial, insira uma descrição ou tema para o curso no campo correspondente.
2. Clique no botão de enviar.
3. O aplicativo retornará uma lista de cinco sugestões de nomes com base no tema fornecido.

## Referência de API
Este aplicativo possui a seguinte rota:
- `GET /`: Renderiza a página inicial e exibe sugestões se uma descrição for enviada via POST.

## Contribuição
Contribuições são bem-vindas! Caso deseje contribuir, siga os passos abaixo:

1. Faça um fork deste repositório.
2. Crie uma nova branch para suas alterações:
   ```bash
   git checkout -b minha-nova-branch
   ```
3. Faça suas alterações e adicione-as:
   ```bash
   git add .
   ```
4. Faça um commit das suas alterações:
   ```bash
   git commit -m "Descrição das alterações"
   ```
5. Envie suas alterações para o repositório remoto:
   ```bash
   git push origin minha-nova-branch
   ```
6. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.