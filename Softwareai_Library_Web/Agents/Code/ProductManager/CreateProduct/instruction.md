


## 🧠 Instrução para o Agente de Product Manager | Create Product
**Objetivo:**  
Ler o preplanejamento para Criar o produto na plataforma financeira stripe utilizando autocreatestripeproduction e tendo como base no documento pre projeto
--- 

## 🔍 Etapas obrigatórias antes da codificação
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo preplanejamento.md para que seja possivel criar nome, valor, moeda e intervalo de cobrança do aplicativo
autogetlocalfilecontent:
- preferred_name: "preplanejamento.md"
- fallback_names: ["preplanejamento.md"]
- search_dir: {doc_md}

### 2️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo keys.env para que seja possivel Salvar ID do Price em STRIPE_SUBSCRIPTION_PRICE_ID_Premium e ID do Produto em STRIPE_PRODUCT_ID_Premium:
autogetlocalfilecontent:
- preferred_name: "keys.env"
- fallback_names: ["keys.env"]
- search_dir: {path_Keys}




## 🔍 Etapas obrigatórias de codificação
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autocreatestripeproduction`  
Para Criar um produto na stripe em modo assinatura 
autocreatestripeproduction:
- nome: Nome do produto
- valor: Valor da assinatura em unidades monetárias (exemplo: 19.99)
- moeda: Código da moeda (ex: brl ou usd), padrão brl
- intervalo: Intervalo de cobrança (day, week, month, year) padrão month (mensal)
- STRIPE_SECRET_KEY: {STRIPE_SECRET_KEY}


### 2️⃣ Executar `autosave`  
Para Salvar ID do Price em STRIPE_SUBSCRIPTION_PRICE_ID_Premium e ID do Produto em STRIPE_PRODUCT_ID_Premium
autosave:
- **path:** {path_Keys}/keys.env
- **code:** conteúdo completo gerado em {path_Keys}/keys.env
