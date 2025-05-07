## 🧠 Instrução Profissional para Geração da Área do Usuário (Painel de Controle)

### Agente: Code Front End Dashboard Product Performance Agent

## 🎯 Objetivo

Gerar um **único arquivo `{path_html}/dashboard.html`** contendo um painel de controle avançado para **Análise de Performance de Produtos**, incluindo:

- **Vendas por SKU**: visualização de quantidade e receita por SKU.
- **Margem de lucro**: cálculo e exibição de margem bruta e líquida por produto.
- **Giro de produto**: métricas de estoque vendido vs tempo, para cada SKU.
- **Comparativo de lançamentos**: análise de desempenho de produtos recém-lançados.
- **Análise de cohort de clientes por categoria**: segmentação de clientes por data de primeira compra e categoria de produto.

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

⚠️ O painel deve refletir exatamente os recursos anunciados em `index.html` relativos a performance de produtos.

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

### 🧩 Menu Lateral - 🏷️ Vendas por SKU
Ao clicar em **Vendas por SKU**, deve aparecer:

- **Tabela de Vendas**:
  - Colunas:
    - 🆔 SKU
    - 🛒 Quantidade vendida
    - 💰 Receita total
    - 📈 Variação % (semana/mês)
    - 🔍 Botão “Ver Detalhes”
- **Cards de Top 5 e Bottom 5**:
  - Destaque para produtos com melhor e pior desempenho.

### 🧩 Menu Lateral - 💹 Margem de Lucro
Ao clicar em **Margem de Lucro**, deve aparecer:

- **Gráfico de Barras**:
  - Margem bruta vs líquida por SKU.
- **Tabela Resumida**:
  - SKU | Receita | Custo | Margem (%) | Status (acima/abaixo da meta).

### 🧩 Menu Lateral - 🔄 Giro de Produto
Ao clicar em **Giro de Produto**, deve aparecer:

- **Indicadores Rápidos**:
  - Média de dias em estoque por SKU.
  - Volume vendido vs estoque inicial.
- **Gráfico de Linha**:
  - Giro ao longo do tempo.

### 🧩 Menu Lateral - 📊 Comparativo de Lançamentos
Ao clicar em **Lançamentos**, deve aparecer:

- **Tabela de Produtos Lançados**:
  - Nome do produto | Data de lançamento | Vendas no período | Comparação com meta.
- **Gráfico de Colunas**:
  - Performance de lançamentos lado a lado.

### 🧩 Menu Lateral - 👥 Cohort de Clientes
Ao clicar em **Cohort**, deve aparecer:

- **Matriz de Cohort**:
  - Linhas: mês/semana de aquisição.
  - Colunas: retenção e LTV médio por categoria.
- **Filtro**:
  - Por categoria de produto e período.

### 🧩 Menu Lateral - ⚙️ Configurações do Painel
Ao clicar em **Configurações**, deve aparecer:

- **Opções de Exibição**:
  - Tema claro/escuro manual
  - Intervalo de atualização automática de dados
- **Usuários e Permissões**:
  - Lista de usuários
  - Definição de papéis (admin, analista)
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

