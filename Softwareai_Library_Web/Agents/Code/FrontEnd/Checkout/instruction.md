
Ao final de sua execução, utilize o Handoffs transfer_to_code_create_navigation_and_refact_frontEnd_agent
Ao final de sua execução, Encaminhe o usuário para o agente de Code Create Navigation And Refact FrontEnd Agent
prossiga com a geração do código front-end específico para o Navigation and Refact
Encaminhe ao agente Code Create Navigation And Refact FrontEnd Agent para criação de navegacao das paginas e algumas refatoracoes
nao utilize <link rel="stylesheet" href="/static/css/global.css"> para definir o estilo da pagina
o estilo da pagina de checkout deve refletir o estilo da pagina index.html
---

voce tem autonomia total para trabalhar nao pergunte se precisa de melhorias ou ajustes
jamais retorne a resposta se autosave estiver disponivel (pois a resposta deve ser o argumento code de autosave possibilitando o salvamento de forma autonoma)

---
### 🧠 Instrução para o Agente de Melhoria de Código Frontend – Página de Checkout

**Objetivo:**  
Crie a **página de checkout** para aquisição de planos. A página deve ser responsiva, clara e com foco em conversão.


## 🔍 Etapas obrigatórias antes de criar página de checkout
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autogetlocalfilecontent`  
para obter o conteudo do argumento NEXT_PUBLIC_STRIPE_PUB_KEY para utilizar em const stripe = Stripe("pk_test_51QpX90Cvm2cRLHtdoF7n2Ea4sRRjYBx8Csiii0e6M6ECTJJ8fKaQ1DKpJApfJZH5hIkWRojaMmaxY9sEcS50tspB00DF2IA12h"); de checkout-payment-button.js`
autogetlocalfilecontent:
  preferred_name: "keys.env"
  fallback_names: ["keys.env"]
  search_dir: {path_Keys}


### 📁 Localização Esperada dos Arquivos checkout.html, checkout-payment-button.js, checkout-payment-selected.js
### 📥 autosave
- **path:** `{path_html}/checkout.html`
- **code:** conteúdo completo gerado de checkout.html
### 📥 autosave
- **path:** `{path_js}/checkout-payment-button.js`
- **code:** conteúdo completo gerado de checkout-payment-button.js
### 📥 autosave
- **path:** `{path_js}/checkout-payment-selected.js`
- **code:** conteúdo completo gerado de checkout-payment-selected.js

---

### ✅ Especificações da Página de Checkout

1. **Layout e Estilo**
- Criar as variáveis globais de estilo do projeto (`:root`).
- Visual limpo e moderno, compatível com **desktop e mobile**.
- Componentes bem espaçados, com bordas arredondadas e destaque nos botões.

2. **Componentes da Página**
- Abaixo de <title> titulo da pagina </title> adicione <script src="https://js.stripe.com/v3/"></script>
- Título: `Complete sua assinatura`
- Subtítulo: `Revise seu plano e finalize o pagamento.`
- Campos de contato:
- Email
- Senha 
- Seletor de opcoes de pagamentos Stripe:
  <div class="option-list">
    <div class="option" data-method="stripe">
      <div class="option-content">
        <div class="control">
          <div class="radio-ui">
            <div class="radio-ui2"></div>
          </div>
        </div>
        <div class="content">
          <div class="primary">
            <div class="text-block">
              <div class="value3">Stripe</div>
            </div>
          </div>

        </div>
      </div>
      <div class="divider3">
        <div class="divider4"></div>
      </div>
    </div>
  </div>

- Botão “Finalizar Pagamento” com classe `.btn-primary`
- Indicador visual de carregamento ao enviar

2. **Funcionalidade Esperada**
- Utilizar o script `checkout-payment-button.js` abaixo como base obrigatória da lógica de pagamento (mesmo o script ja existindo o salve na Localização Esperada dos Arquivos) 
### 🔐 Script Base (checkout-payment-button.js)
```javascript
{checkout_payment_button_js}
```

3. **Funcionalidades Esperadas**
- Utilizar o script `checkout-payment-selected.js` abaixo como base obrigatória da lógica de selecao de pagamento (mesmo o script ja existindo o salve na Localização Esperada dos Arquivos) 
### 🔐 Script Base (checkout-payment-selected.js)
```javascript
{checkout_payment_selected_js}
```
