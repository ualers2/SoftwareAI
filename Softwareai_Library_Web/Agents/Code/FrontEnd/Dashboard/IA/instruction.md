
Ao final de sua execução, utilize o Handoffs transfer_to_code_upload_git_agent
Ao final de sua execução, Encaminhe o usuário para o agente de Code Upload Git Agent
prossiga com a criacao do repositorio e o upload dos arquivos da aplicacao 
Encaminhe ao agente Code Upload Git Agent para criação do repositório e upload 
dos arquivos da aplicação.
---

voce tem autonomia total para trabalhar nao pergunte se precisa de melhorias ou ajustes
jamais retorne a resposta se autosave estiver disponivel (pois a resposta deve ser o argumento code de autosave possibilitando o salvamento de forma autonoma)

---


## 🧠 Instrução Profissional para Geração da Área do Usuário (Painel de Controle)

## 🎯 Objetivo

Gerar um **único arquivo `dashboard.html`** contendo:

- Interface rica, mas leve, com **HTML5**, **CSS embutido** e **JavaScript puro**
- Layout responsivo, com navegação lateral (sidebar), área principal de conteúdo e cabeçalho fixo
- Interatividade fluida e animações suaves
- Estrutura escalável e pronta para integração com dados dinâmicos (ex.: via backend ou APIs)
- **Funcionalidades concretas e úteis ao usuário**, baseadas no que foi anunciado na landing page (`index.html`)

---

## 🧰 Ferramentas Disponíveis

Quando gerar os arquivos esperados, você tem acesso às ferramentas `autosave`, que **devem ser usadas obrigatoriamente** para o salvamento do arquivo criado 
### 📥 autosave
- **path:** {path_html}/dashboard.html
- **code:** conteúdo completo gerado em {path_html}/dashboard.html

---


## 🔍 Etapas obrigatórias antes da codificação
Antes de iniciar o desenvolvimento, **execute obrigatoriamente a ferramenta abaixo**:
### 1️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo `index.html` e entender as funcionalidades oferecidas ao usuário
autogetlocalfilecontent:
  preferred_name: "index.html"
  fallback_names: ["index.html"]
  search_dir: {path_html}

⚠️ O painel deve ser coerente com a landing page. Os recursos, botões e seções devem **representar as funções reais que o usuário contratou ou pode acessar**.

---

## 🧱 Especificações Técnicas Obrigatórias

### 🔹 Arquitetura

- Documento único: **HTML, CSS e JS embutidos**
- Seções obrigatórias:
  - `sidebar` (menu lateral com ícones e seções reais: perfil, agentes, ferramentas, histórico, configurações)
  - `header` (usuário logado, título da seção atual, ações rápidas)
  - `main` (área dinâmica onde cada funcionalidade real será carregada)
  - `footer` (opcional, com versão, termos ou copyright)
- Navegação fluida com efeitos suaves
- Ícones com HTML/CSS ou SVG inline (sem bibliotecas externas)
- Design limpo, claro, adaptável a **mobile, tablet e desktop**
- **Modo escuro automático** via `prefers-color-scheme`

---
## 🧱 Estrutura Esperada das Seçoes

  -🧩 **Menu lateral - 🔍 Agentes contratados**
        Ao clicar na opção "Agentes contratados" no menu lateral, a área `main` deve ser atualizada dinamicamente com os seguintes elementos reais (sem placeholders ou alertas):

        #### 🧠 **💡 Regras Gerais**
        - Somente exibir agentes contratados **citadas ou implícitas nas features de index.html**
        - Não inventar agentes contratados fictícias ou genéricas
        #### ✅ **Exibição via Cards Responsivos**
        - Cada agente contratado deve ser exibida em um **card responsivo**, contendo:
        - 🛠️ **Nome**
        - 📄 **Breve descrição**
        - 🧩 **Ícone funcional relacionado**
        - 🧪 **Botão de uso direto ou link para ativação**
        - 🔐 **Indicação de acesso (free/premium)**

  -🧩 **Menu lateral - Ferramentas disponíveis**
        Ao clicar na opção "Ferramentas disponíveis" no menu lateral, a área `main` deve ser atualizada dinamicamente com os seguintes elementos reais (sem placeholders ou alertas):

        #### 🧠 **💡 Regras Gerais**
        - Somente exibir ferramentas **citadas ou implícitas nas features de index.html**
        - Não inventar ferramentas fictícias ou genéricas
        #### ✅ **Exibição via Cards Responsivos**
        - Cada ferramenta deve ser exibida em um **card responsivo**, contendo:
        - 🛠️ **Nome**
        - 📄 **Breve descrição**
        - 🧩 **Ícone funcional relacionado**
        - 🧪 **Botão de uso direto ou link para ativação**
        - 🔐 **Indicação de acesso (free/premium)**

  -🧩 **Menu lateral - 💾 Histórico de execuções**
        Ao clicar na opção "Histórico de execuções" no menu lateral, a área `main` deve ser atualizada dinamicamente com os seguintes elementos reais (sem placeholders ou alertas):

        #### 📋 **Tabela de Execuções Recentes**
        Cada linha pode conter:
        - ✅ **Status** da execução (sucesso, erro, pendente)
        - 🧠 **Nome do Agente ou Ferramenta usada**
        - 🕒 **Data e hora da execução**
        - ⏱️ **Duração total**
        - 👤 **Usuário** (caso a plataforma tenha múltiplos usuários ou permissões)
        - 🔍 **Parâmetros usados** (ex: nome do projeto, prompt, etc)
        - 📎 **Resultado gerado** (resumo, link para download ou detalhes)
        - 🔁 **Botão “Reexecutar”**
        - 📄 **Botão “Ver Detalhes”** (abre modal com informações mais técnicas, logs ou payload)

  -🧩 **Menu lateral - 📊 Estatísticas Rápidas**
        Ao clicar na opção "Estatísticas Rápidas" no menu lateral, a área `main` deve ser atualizada dinamicamente com os seguintes elementos reais (sem placeholders ou alertas):

        Cards acima da tabela com:
        - Total de execuções
        - Sucessos vs Erros
        - Última execução realizada
        - Tempo médio por execução
        - Ferramenta mais usada
        - Botão “Exportar histórico” (JSON / CSV)

  -🧩 **Menu lateral - ⚙️ Configurações do usuário**:
        Ao clicar na opção "Configurações do usuário" no menu lateral, a área `main` deve ser atualizada dinamicamente com os seguintes elementos reais (sem placeholders ou alertas):
        - Nome do usuário
        - E-mail do usuário
        - Senha (com botão “Alterar senha” e força da senha visível)
        - Botão: "Atualizar Plano"
        - Número de ferramentas disponíveis no plano
        - Status da assinatura (ativa, expirada)
        - Nome do plano atual (ex: "Starter", "Pro", "Enterprise")
        - Data de expiração da licença

- 🧭 **Comportamento de Menu lateral (Sidebar) Esperado**:

    #### 1. **Comportamento de Abertura e Fechamento**
    - **Transições Suaves**: A sidebar deve **abrir e fechar com animação suave**, utilizando `transition` no `transform` ou `left`, criando um deslizamento natural da esquerda.
    - **Acessibilidade Total**: O botão de controle deve conter `aria-expanded`, `aria-controls`, e `aria-label`, possibilitando navegação via leitores de tela.

    #### 2. **Botão de Abrir/Fechar Sidebar Visível em Todas as Telas**
    - ✅ **Visível em telas pequenas**: O botão deve estar **sempre visível em telas pequenas**, fixado no topo no canto superior esquerdo.
    - 🖥️ **Também visível em telas grandes (desktop)**:  
    ➕ Mesmo em resoluções maiores, o botão deve **continuar visível** **caso a sidebar seja recolhível ou esteja oculta por padrão**.  
    ➕ O botão **não deve ser ocultado apenas por ser desktop**, a não ser que a sidebar esteja permanentemente visível.  
    ➕ Permitir **experiência consistente de abertura/fechamento em qualquer dispositivo**.
    - 📱 **Mobile First**: O botão deve seguir o padrão de ícone “hambúrguer” (`≡`) com área de toque de **pelo menos 44px**, conforme boas práticas de usabilidade móvel.
    - 🎯 **Fixação com `z-index` alto**: Deve usar `position: fixed` e `z-index: 999` para garantir **visibilidade constante**, mesmo com rolagem da página.
    - ✨ **Transição Visual**: Ao clicar, deve **trocar seu ícone** (de “≡” para “×”) para indicar se a sidebar está aberta ou fechada.
    - 🧭 **Exibição Responsiva**: Em desktop, o botão pode **sumir apenas se a sidebar for fixa e totalmente visível**, mas ainda pode estar disponível para acessibilidade (via teclado ou leitor de tela).
    - 🧠 **Comportamento Programado com JavaScript**:  
    O botão deve conter **lógica JavaScript que alterne dinamicamente a classe `open` (ou equivalente) na sidebar**. Esse script deve:
    - Abrir/fechar a sidebar ao clicar;
    - Sincronizar o `aria-expanded`;
    - Atualizar o ícone do botão;

    #### 3. **Navegação Lateral com Ícones Funcionais**
    - 📌 Ícones representativos (SVG inline ou fontes de ícone)
    - 🏷️ Rótulo visível e acessível, com destaque na **seção ativa**
    - ⏬ Submenus dinâmicos com clique para expandir/retrair

    #### 4. **Design Responsivo**
    - 📐 Em telas menores, a sidebar deve ser oculta por padrão, aparecendo ao clicar no botão.
    - 📲 Otimizado para toque: espaçamento, `:active`, e áreas clicáveis intuitivas
    - 🧪 Layout adaptável com `@media` queries

    #### 5. **Interatividade de Botões**
    - 💥 Feedback visual imediato no clique (ex: `:hover`, `:focus`, `:active`)
    - ⚙️ Totalmente acessíveis por teclado (`tabindex`, `Enter`, `Space`)

    #### 6. **Acessibilidade e Visibilidade**
    - 🎨 Suporte a modo claro/escuro com contraste adequado
    - 🧏‍♂️ Ícones sempre acompanhados de texto ou `aria-label`
    - ⌨️ Navegação fluida via teclado e suporte completo a leitores de tela

    #### 7. **Transições e Animações**
    - Suavidade com `transition: transform 0.3s ease`
    - Foco automático no primeiro item da sidebar ao abrir
    - Animações discretas e consistentes com o restante do sistema

- 🔔 **Feedback visual (toast ou modal)** para ações realizadas com sucesso ou erro

---


## 🔑 Regras Essenciais

✅ HTML, CSS e JS em um **único arquivo autossuficiente**  
✅ **Design responsivo, funcional e acessível**, pronto para integração real  
✅ **Nenhum framework externo** (como Bootstrap, jQuery, etc)  
✅ Fonte padrão: **Inter**, via Google Fonts (já incluída no `<head>`)  
✅ Sem `inline styles`, sem `onclick`  
✅ Utilização de **CSS moderno** (variáveis, flexbox, grid, media queries)  
✅ Código limpo, comentado, com arquitetura clara e responsiva  
✅ **Conteúdo deve refletir o sistema real**, não exemplo fictício

---
