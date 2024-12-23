
# Documentação do Projeto de Análise Técnica de Bitcoin 🪙

## 📚 Introdução
Este projeto tem como objetivo criar um script em Python para a análise técnica da criptomoeda Bitcoin. O foco principal é coletar dados históricos de preços, calcular indicadores técnicos (como Médias Móveis, RSI e MACD) e gerar gráficos interativos.

### Funcionalidades-chave:
- Coleta de dados históricos de preços do Bitcoin através de uma API.
- Cálculo de indicadores técnicos: Média Móvel (MA), Índice de Força Relativa (RSI) e MACD.
- Geração de gráficos interativos utilizando Matplotlib.

---

## ⚙️ Instalação
### Requisitos do Sistema
- Python 3.6 ou superior.
- Bibliotecas:
  - `requests`
  - `pandas`
  - `matplotlib`
  - `numpy`

### Dependências Necessárias
Para instalar as dependências, execute o seguinte comando:
```bash
pip install requests pandas matplotlib numpy
```

### Guia Passo-a-Passo
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu_usuario/repositorio.git
   cd repositorio
   ```
2. **Instale as dependências conforme listado acima.**
3. **Execute o script:**
   ```bash
   python seu_script.py
   ```

### Configuração Inicial
A configuração inicial requer apenas que você confirme que todas as bibliotecas foram instaladas. Não há necessidade de nenhuma configuração adicional no script para a instalação.

---

## 🛠️ Uso
### Exemplos Práticos
1. **Executar o script para coletar e plotar dados:**
   ```bash
   python seu_script.py
   ```

### Comandos Principais
- O script é executado ao chamar a função `main()`.

### Configurações Disponíveis
Atualmente, os períodos para cálculos são fixos, mas podem ser ajustados diretamente nas funções:
- `calculate_moving_average(df, window=14)`
- `calculate_rsi(df, period=14)`

### Casos de Uso Comuns
- Análise de tendências de preços do Bitcoin.
- Avaliação de sinais de compra/venda com base em indicadores técnicos.

---

## 📁 Estrutura do Projeto
```plaintext
projeto/
│
├── seu_script.py             # Código principal do script
├── README.md                  # Documentação do projeto
└── requirements.txt           # Dependências do projeto
```

---

## 📡 API
### Endpoints Disponíveis
- **URL:** `https://api.coindesk.com/v1/bpi/historical/close.json`

### Métodos e Parâmetros
- **GET:** `https://api.coindesk.com/v1/bpi/historical/close.json`
    - Retorna dados de preços históricos do Bitcoin.

### Exemplos de Requisições
```python
response = requests.get(API_URL)
```

### Respostas Esperadas
- Um JSON contendo dados das datas e preços do Bitcoin.

---

## 🤝 Contribuição
### Guia para Contribuidores
- Faça um fork do repositório.
- Crie uma branch para suas alterações:
  ```bash
  git checkout -b feature/nova-funcionalidade
  ```
- Envie um pull request explicando suas alterações.

### Padrões de Código
- Siga o estilo PEP 8 para Python.
- Adicione comentários explicativos no código.

### Processo de Pull Request
1. Realize suas modificações.
2. Teste seu código.
3. Abra um pull request para revisão.

### Boas Práticas
- Mantenha o código modular.
- Documente cada função e classe utilizando docstrings.

---

## 📜 Licença
### Tipo de Licença
Este projeto está licenciado sob a Licença MIT.

### Termos de Uso
Permite o uso, cópia, modificação e distribuição, desde que a atribuição ao autor original seja mantida.

### Restrições
Não é permitido o uso do nome do autor para fins promocionais sem permissão prévia.

---

## 🔄 Manutenção Contínua
- Atualizações do projeto serão feitas conforme novas funcionalidades forem necessárias.
- Revisões de código serão realizadas periodicamente.

Obrigado por escolher o projeto de Análise Técnica de Bitcoin! Se você tiver alguma dúvida ou sugestão, não hesite em entrar em contato! 😊