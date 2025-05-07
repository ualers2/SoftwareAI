## 🧠 Instrução Profissional para Geração da Área do Usuário (Painel de Controle)

### Agente: Code Front End Dashboard Supply Chain Agent

## 🎯 Objetivo

Gerar um **único arquivo `{path_html}/dashboard.html`** contendo um painel de controle voltado para **Monitoramento da Cadeia de Suprimentos**, com as seguintes funcionalidades:

- **Níveis de estoque em várias localidades**: visão consolidada e detalhada por depósito/região.
- **Status de pedidos a fornecedores**: acompanhamento de pedidos pendentes, em trânsito e recebidos.
- **Lead times**: cálculo e visualização de tempos médios de processamento e transporte.
- **Gargalos logísticos**: identificação de pontos críticos e atrasos em fluxos de suprimento.
- **KPIs de eficiência**: métricas como Fill Rate, OTIF (On Time In Full), giro de estoque e custo logístico.

O painel deve ser leve, responsivo e interativo, pronto para integração com dados dinâmicos via backend ou APIs.

---

## 🧰 Ferramentas Disponíveis

Ao gerar o arquivo, utilize obrigatoriamente a ferramenta `autosave` para salvar o resultado gerado:

### 📥 autosave
- **path:** `{path_html}/dashboard.html`
- **code:** conteúdo completo do dashboard

---

## 🔍 Etapas obrigatórias antes da codificação

1️⃣ **Executar `autogetlocalfilecontent`** para obter o conteúdo completo de `index.html` e alinhar o design e funcionalidades do painel com a landing page.
```yaml
autogetlocalfilecontent:
  preferred_name: "index.html"
  fallback_names: ["index.html"]
  search_dir: {path_html}
```

⚠️ O painel deve refletir exatamente os recursos anunciados em `index.html` referentes ao supply chain.

---

## 🧱 Especificações Técnicas Obrigatórias

- **Documento único**: HTML5, CSS embutido e JavaScript puro num só arquivo.
- **Layout**: responsivo, com sidebar, header fixo, área principal dinâmica e footer opcional.
- **Modo escuro automático** via `prefers-color-scheme`.
- **Sem frameworks externos** ou bibliotecas: ícones em SVG inline ou CSS.
- **Fontes**: Inter via Google Fonts (já incluída no `<head>`).
- **Acessibilidade**: uso de `aria-` attributes, navegação por teclado e contraste adequado.
- **CSS Moderno**: variáveis, flexbox, grid e media queries.

---

## 🧱 Estrutura Esperada das Seções

### 🧩 Menu Lateral - 📦 Estoque por Localidade
Ao clicar em **Estoque por Localidade**, deve aparecer:

- **Visão Geral Consolidada**:
  - Cards resumindo cada depósito/região:
    - 📍 Localidade (nome do depósito)
    - 📦 Total de itens em estoque
    - 🔻 Alerta para itens abaixo do nível mínimo
    - 🧠 Botão para detalhes
- **Tabela Detalhada**:
  - Colunas:
    - 🆔 Item
    - 📦 Quantidade em estoque
    - 🔢 Ponto de pedido
    - 📦 Mínimo/Ideal
    - 🔍 Botão “Ver Histórico de Movimentações”

### 🧩 Menu Lateral - 📝 Pedidos a Fornecedores
Ao clicar em **Pedidos**, deve aparecer:

- **Status por Pedido**:
  - Lista ou cards com cada pedido:
    - 🆔 Nº do pedido
    - 🏭 Fornecedor
    - 📅 Data de emissão
    - 🚚 Status (pendente, em trânsito, recebido)
    - ⏳ Lead time estimado vs real
    - 🔍 Botão “Ver Detalhes”
- **Filtro Rápido**:
  - Por status, data e fornecedor

### 🧩 Menu Lateral - 🚚 Gargalos e Lead Times
Ao clicar em **Logística**, deve aparecer:

- **Gráfico de Lead Times**:
  - Linha ou barras mostrando tempos médios diários/semanas
- **Mapa de Gargalos** (simplificado SVG ou Canvas)
  - Indicadores visuais nos pontos de maior atraso
- **Lista de Alertas**:
  - Pontos com lead time acima do SLA
    - 📍 Localidade
    - ⏱️ Tempo registrado
    - 📝 Ação recomendada

### 🧩 Menu Lateral - 📊 KPIs de Eficiência
Ao clicar em **KPIs**, deve aparecer:

- **Cards de Métricas**:
  - 📈 Fill Rate (%)
  - ⏰ OTIF (%)
  - 🔄 Giro de Estoque (dias)
  - 💰 Custo Logístico (R$)
- **Gráfico de Tendência**:
  - Curva de cada KPI ao longo do tempo
- **Botão “Exportar Relatório”** (JSON / CSV)

### 🧩 Menu Lateral - ⚙️ Configurações do Painel
Ao clicar em **Configurações**, deve aparecer:

- **Opções de Exibição**:
  - Tema claro/escuro manual
  - Intervalo de atualização automática de dados
- **Usuários e Permissões**:
  - Lista de usuários
  - Definição de papéis (admin, operador)
  - Botões de adicionar/remover usuários

---

## 🔑 Regras Essenciais

✅ **Único arquivo**: HTML, CSS e JS sem dependências externas.
✅ **Responsividade** e **acessibilidade** garantidas.
✅ **Design fiel** à landing page.
✅ **Sem inline styles** e **sem atributos `onclick`**.
✅ **Código limpo** e bem comentado.

---

<!-- Ao terminar, a ferramenta autosave deve ser executada automaticamente pelo sistema -->

