
# 🌟 Introdução
Este projeto é um **Analisador de Dados CSV**, desenvolvido em Python. O principal objetivo é permitir a leitura, processamento e análise de dados a partir de arquivos CSV. Entre as funcionalidades principais estão a remoção de valores nulos, a normalização dos dados e a geração de estatísticas básicas, além de relatórios gráficos.

# ⚙️ Instalação
Para instalar e executar o projeto, você precisará das seguintes dependências e de um ambiente Python configurado:

1. **Requisitos do sistema**:  
   - Python 3.x  
   - pip

2. **Dependências necessárias**:  
   - `pandas`  
   - `numpy`  
   - `matplotlib`  
   - `seaborn`

3. **Guia passo-a-passo**:  
   1. Clone este repositório:  
      ```  
      git clone https://github.com/seu_usuario/CSVDataAnalyzer.git  
      ```  
   2. Navegue até o diretório do projeto:  
      ```  
      cd CSVDataAnalyzer  
      ```  
   3. Instale as dependências:  
      ```  
      pip install -r requirements.txt  
      ```

# 🎮 Uso
Para utilizar o **CSVDataAnalyzer**, siga os exemplos abaixo:

1. **Exemplo prático**:  
   ```python  
   from CSVDataAnalyzer import CSVDataAnalyzer  

   analyzer = CSVDataAnalyzer("caminho/para/seu/arquivo.csv")  
   analyzer.read_csv()  
   analyzer.preprocess_data()  
   stats = analyzer.basic_statistics()  
   if stats:  
       print("Estatísticas Básicas:", stats)  
   analyzer.generate_report()  
   ```

2. **Comandos principais**:  
   - `read_csv()`: Lê o arquivo CSV.  
   - `preprocess_data()`: Processa os dados.  
   - `basic_statistics()`: Gera estatísticas básicas.  
   - `generate_report()`: Gera gráficos de distribuição.

3. **Configurações disponíveis**:  
   A inicialização do `CSVDataAnalyzer` requer o caminho do arquivo CSV a ser analisado.

4. **Casos de uso comuns**:  
   - Análise de datasets para relatórios de negócios.  
   - Pré-processamento de dados para Machine Learning.

# 📜 Estrutura do Projeto
- `analyzer.py`: Contém a classe `CSVDataAnalyzer`.  
- `requirements.txt`: Lista de dependências do projeto.  
- `README.md`: Documentação do projeto.

# 🔌 API
Os principais métodos disponíveis na classe `CSVDataAnalyzer` são:  
- `read_csv()`: Lê e armazena dados do arquivo CSV.  
- `preprocess_data()`: Normaliza os dados e remove valores nulos.  
- `basic_statistics()`: Retorna estatísticas básicas (média, mediana, etc.).  
- `generate_report()`: Gera gráficos utilizando `matplotlib` e `seaborn`.

# 🤝 Contribuição
Para contribuir com o projeto, siga os passos abaixo:

1. **Guia para contribuidores**:  
   - Faça um fork do repositório.  
   - Crie sua branch (`git checkout -b feature/SuaFeature`).  
   - Faça suas alterações e teste.  
   - Submeta um Pull Request.

2. **Padrões de código**:  
   - Mantenha a consistência de estilo conforme a PEP 8.

3. **Boas práticas**:  
   - Não envie código quebrado.  
   - Teste suas mudanças antes de enviar.

# 📜 Licença
Este projeto está licenciado sob a MIT License. Consulte o arquivo LICENSE para obter mais detalhes sobre termos de uso e restrições.