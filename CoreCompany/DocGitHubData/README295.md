# 📈 Análise Técnica da Ethereum

## 🌟 Introdução
Este projeto visa criar uma ferramenta que permita realizar análises técnicas da criptomoeda Ethereum. Através da coleta de dados de preços históricos e do cálculo de diversos indicadores, como médias móveis, Índice de Força Relativa (RSI) e bandas de Bollinger, fornecemos uma solução robusta para auxiliar tomadas de decisão em investimentos.

### Funcionalidades-Chave
- Coleta de dados históricos de preços da Ethereum.
- Cálculo de indicadores técnicos.
- Visualização dos indicadores através de gráficos intuitivos.

---

## ⚙️ Instalação

### Requisitos do Sistema
- Python 3.7 ou superior.
- Bibliotecas: `requests`, `pandas`, `numpy`, `matplotlib`.

### Dependências Necessárias
```bash
pip install requests pandas numpy matplotlib
```

### Guia Passo-a-Passo
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/usuario/repo.git
   ```
2. **Navegue até o diretório do projeto:**
   ```bash
   cd repo
   ```
3. **Instale as dependências:** (ver seção acima)
4. **Execute o script Python:**
   ```bash
   python seu_script.py
   ```

### Configuração Inicial
Não há configuração inicial necessária além da instalação das dependências.

---

## 🛠️ Uso

### Exemplos Práticos
Para gerar a análise técnica, basta executar o script. Ele coleta dados por 30 dias por padrão e calcula os indicadores.

### Comandos Principais
- `analysis.collect_data(days=30)`: Coleta dados de preços dos últimos 30 dias.
- `analysis.calculate_moving_average(window=7)`: Calcula a média móvel com uma janela de 7 dias.
- `analysis.plot_data()`: Gera os gráficos com os dados analisados.

### Configurações Disponíveis
Você pode alterar:
- `days` nos métodos para coletar dados para diferentes períodos.
- `window` para o cálculo dos indicadores.

### Casos de Uso Comuns
- Análise diária dos preços da Ethereum.
- Monitoramento de tendências através de médias móveis e RSI.
- Visualização dos dados com gráficos informativos.

---

## 🗂️ Estrutura do Projeto

```
/análise-técnica-ethereum
│
├── script.py                # Código fonte principal
└── README.md                # Documentação do projeto
```

---

## 📡 API

### Endpoints Disponíveis
- **Coingecko API**
  - Utilizada para coletar dados históricos de preços da Ethereum.
  
### Métodos e Parâmetros
- `GET /coins/{symbol}/market_chart`:
  - **`vs_currency`**: moeda usada para conversão (ex: usd).
  - **`days`**: número de dias para coletar os dados.

### Exemplos de Requisições
```python
url = f"https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days=30"
```

### Respostas Esperadas
- Dados de preços em formato JSON contendo timestamps e preços da criptomoeda.

---

## 🤝 Contribuição

### Guia para Contribuidores
Contribuições são bem-vindas! Siga este processo básico:
1. Faça um fork do repositório.
2. Crie uma nova branch para suas funcionalidades (`git checkout -b feature/novaFuncionalidade`).
3. Faça suas alterações e commit (`git commit -m 'Adiciona nova funcionalidade'`).
4. Envie suas alterações (`git push origin feature/novaFuncionalidade`).
5. Abra um Pull Request.

### Padrões de Código
- Utilize o PEP 8 como guia para formatação e estilo de código.
  
### Boas Práticas
- Mantenha a documentação atualizada.
- Escreva testes para suas novas funcionalidades.

---

## 📄 Licença

### Tipo de Licença
Este projeto está licenciado sob a Licença MIT.

### Termos de Uso
- Uso pessoal e acadêmico é permitido.
- Para fins comerciais, entre em contato com o mantenedor do projeto.

### Restrições
- É proibido redistribuir o código sem o devido creditamento ao autor original.

---

## 🔄 Manutenção Contínua
A documentação será mantida de acordo com as atualizações e novas funcionalidades do software. Revisões periódicas serão realizadas para garantir a precisão e a clareza das informações aqui contidas.

## 🤝 Colaboração
A integração contínua com a equipe, participação em reuniões e feedback são fundamentais para o sucesso do projeto.

Por favor, sinta-se à vontade para entrar em contato se você tiver dúvidas ou precisar de assistência.