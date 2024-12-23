
# Documentação do Projeto - Análise Técnica de Criptomoedas 🪙

## 1. 📚 Introdução

Bem-vindo à documentação do nosso projeto de desenvolvimento de um script para a análise técnica de criptomoedas. Este projeto tem como objetivo facilitar a compra e venda de ativos digitais com base em indicadores de mercado, aumentando a acurácia nas decisões financeiras.

### Funcionalidades-chave:
- **Cálculo de Médias Móveis (MA)**
- **Cálculo do Índice de Força Relativa (RSI)**
- **Cálculo de Bandas de Bollinger**
- **Análise de dados históricos**
- **Geração de relatórios de tendência**

---

## 2. ⚙️ Instalação

### Requisitos do Sistema
- **Python 3.x**
- **Pacotes Necessários** (consultar dependências)

### Dependências Necessárias
- `numpy`
- `pandas`
- `matplotlib`
- `scipy`

### Guia Passo-a-Passo
1. Clone o repositório:
   ```bash
   git clone https://github.com/usuario/repo.git
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd repo
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Configuração Inicial
1. Configure suas chaves de API, se necessário (para coleta de dados).
2. Ajuste as configurações padrão no arquivo `config.json`.

---

## 3. 🔍 Uso

### Exemplos Práticos
```python
from analise_criptomoedas import calcular_rsi, calcular_ma, gerar_relatorio

# Carregar dados
dados = carregar_dados('dados.csv')

# Cálculo de indicadores
rsi = calcular_rsi(dados)
ma = calcular_ma(dados)

# Gerar relatório
gerar_relatorio(dados, ma, rsi)
```

### Comandos Principais
- **`calcular_rsi(dados)`**: Retorna o Índice de Força Relativa.
- **`calcular_ma(dados)`**: Retorna as Médias Móveis.
- **`gerar_relatorio(dados, ma, rsi)`**: Gera um relatório baseado nos dados e indicadores.

### Configurações Disponíveis
- Ajustar períodos para `calculate_ma`.
- Definir limites para cálculo do RSI.

### Casos de Uso Comuns
- Análise diária de criptomoedas.
- Geração de relatórios semanais para investidores.

---

## 4. 📁 Estrutura do Projeto
```plaintext
análise-criptomoedas/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── analise_criptomoedas.py
│   └── utils.py
│
├── data/
│   ├── dados.csv
│
├── requirements.txt
├── config.json
└── README.md
```

---

## 5. 🌐 API

### Endpoints Disponíveis
- **`/api/rsi`**: Retorna o Índice de Força Relativa.
- **`/api/ma`**: Retorna as Médias Móveis.
- **`/api/relatorio`**: Gera um relatório com base nos dados.

### Métodos e Parâmetros
- **`GET /api/rsi?periodo=14`**
- **`GET /api/ma?periodo=20`**
- **`POST /api/relatorio`**

### Exemplos de Requisições
```bash
curl -X GET "http://localhost:8000/api/rsi?periodo=14"
```

### Respostas Esperadas
```json
{
  "rsi": 67.5
}
```

---

## 6. 🤝 Contribuição

### Guia para Contribuidores
Se você deseja contribuir para este projeto, siga os passos abaixo:
1. **Fork** o projeto.
2. Crie uma nova branch:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```
3. Faça suas alterações e envie um Pull Request.

### Padrões de Código
- Siga o **PEP 8** para formatação de código Python.
- Inclua testes unitários para novas funcionalidades.

### Processo de Pull Request
- Certifique-se de que seu código esteja testado.
- Forneça uma descrição clara do que o Pull Request altera.

### Boas Práticas
- Mantenha a documentação sempre atualizada.
- Comentários claros em trechos complexos de código.

---

## 7. 📝 Licença

### Tipo de Licença
Este projeto está licenciado sob a **MIT License**.

### Termos de Uso
- Você pode usar, copiar, modificar e distribuir o software, desde que inclua uma cópia da licença.

### Restrições
- Não é permitido usar o software para fins ilegais.

---

## 8. 📆 Roadmap
**Roadmap do Projeto - Análise Técnica de Criptomoedas**

- **Fase 1: Levantamento de Requisitos**  
  Data: 2024-11-12 a 2024-11-16  
- **Fase 2: Desenvolvimento do Script**  
  Data: 2024-11-17 a 2024-12-01  
- **Fase 3: Testes e Validação**  
  Data: 2024-12-02 a 2024-12-10  
- **Fase 4: Implantação**  
  Data: 2024-12-11 a 2024-12-15  
- **Fase 5: Avaliação Pós-Implantação**  
  Data: 2024-12-16 a 2024-12-20  

---

Essa documentação deverá ser atualizada regularmente à medida que novas funcionalidades e alterações forem implementadas. Se houver dúvidas ou sugestões, sinta-se à vontade para entrar em contato na seção de discussões do repositório! 💬