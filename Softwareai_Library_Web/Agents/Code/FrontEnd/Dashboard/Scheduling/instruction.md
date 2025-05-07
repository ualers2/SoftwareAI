
Ao final de sua execução, utilize o Handoffs transfer_to_code_upload_git_agent
Ao final de sua execução, Encaminhe o usuário para o agente de Code Upload Git Agent
prossiga com a criacao do repositorio e o upload dos arquivos da aplicacao 
Encaminhe ao agente Code Upload Git Agent para criação do repositório e upload 
dos arquivos da aplicação.
---

voce tem autonomia total para trabalhar nao pergunte se precisa de melhorias ou ajustes
jamais retorne a resposta se autosave estiver disponivel (pois a resposta deve ser o argumento code de autosave possibilitando o salvamento de forma autonoma)

---


## 🧠 Instrução Profissional para Geração da Área do Usuário (Painel de Controle - Agendador de Posts)

## 🎯 Objetivo

Gerar um **único arquivo `dashboard.html`** contendo:

- HTML5, CSS embutido e JavaScript puro (sem dependências externas)
- Interface moderna, estilosa e responsiva, com foco na experiência do usuário
- Visual intuitivo para agendamento, gerenciamento e análise de posts
- Estrutura preparada para integração futura com APIs de redes sociais (Instagram, TikTok, YouTube, Twitter)

---

## 🧰 Ferramentas Disponíveis

Você pode usar a ferramenta `autosave`, obrigatoriamente, para salvar o arquivo gerado.  
### 📥 autosave
- **path:** `{path_html}/dashboard.html`
- **code:** conteúdo completo gerado em `{path_html}/dashboard.html`

---

## 🔍 Etapas obrigatórias antes da codificação

### 1️⃣ Executar `autogetlocalfilecontent`
autogetlocalfilecontent:
  preferred_name: "index.html"
  fallback_names: ["index.html"]
  search_dir: {path_html}

⚠️ O painel deve refletir **exatamente os recursos de <!-- Features Section --> em `index.html`**.

---

## 🧱 Especificações Técnicas
### 🔹 Estrutura do Painel

O `dashboard.html` deve conter:

- **`<sidebar>`**: menu lateral com ícones elegantes e seções funcionais:
  - Agendador
  - Agentes
  - Histórico
  - Configurações

- **`<header>`**: barra superior com:
  - Nome do usuário logado
  - Título da seção atual

- **`<main>`**: área dinâmica que carrega os conteúdos de cada seção via JavaScript

- **`<footer>`**: versão do sistema e créditos discretos

### 🔹 Requisitos Visuais

- Design clean, profissional, com uso inteligente de cores e espaçamento
- Efeitos de transição suaves entre seções
- Ícones SVG inline ou com HTML/CSS (sem bibliotecas externas)
- Suporte completo a **modo escuro automático** via `prefers-color-scheme`
- Totalmente responsivo: adaptável a telas **mobile, tablet e desktop**


### ✅ Importante

🔸 **Cada seção do menu deve carregar conteúdo funcional real na área `main`, sem usar `alert()` ou mensagens fictícias.**  
🔸 A navegação deve trocar o conteúdo dinamicamente com JavaScript, **exibindo os elementos reais de cada área conforme as especificações abaixo.**
🚫 **Não utilizar `alert()` ou placeholders genéricos.**

---

## 🔹 Elementos Esperados para Agendador de Post

🎯 Recursos concretos para **criação e agendamento de publicações** em redes sociais:



### Menu lateral - 📝 Agendador de Postagem
- 📊 Cards com Estatísticas Visuais:
  - Total de posts agendados
  - Posts por rede
  - Último post enviado
  - Indicador de erros recentes
- 🗓️ Calendário de Agendamentos
  - Visualização das datas:
    - semanal com navegação para proximas semanas 
    Codigo base:
    <div class="calendar">
        <div class="calendar-header"><button id="prev-month">&#8249;</button><div id="month-year"></div><button id="next-month">&#8250;</button></div>
        <div class="days"><div class="day">D</div><div class="day">S</div><div class="day">T</div><div class="day">Q</div><div class="day">Q</div><div class="day">S</div><div class="day">S</div></div>
        <div class="dates" id="calendar-dates"></div>
    </div>
    <button class="btn" id="open-schedule">Agendar Posts</button>

  - Clique em uma ou varias data e depois em Botao "Agendar Posts" e se abrirá um modal para visualizar e adicionar posts:
    - Seleção da rede social
    - Campo de titulo (que a ia ira preencher)
    - Campo de descrições (que a ia ira preencher)
    - Simulação de upload de imagem ou vídeo
    - Escolha de data definida pelo Calendário com uma ou varias datas 
    - Escolha de hora
    - Botão “Agendar Post” estilizado
    Codigo base:
    <div class="modal-content">
      <button class="close" data-close>&times;</button>
      <h3>Agendar Post</h3>
      <div class="form-group"><label>Rede Social</label><select><option>YouTube</option><option>TikTok</option><option>Twitter</option><option>Instagram</option></select></div>
      <div class="form-group"><label>Título</label><input type="text" /></div>
      <div class="form-group"><label>Descrição</label><textarea rows="3"></textarea></div>
      <div class="form-group"><label>Imagem/Vídeo</label><input type="file" accept="image/*,video/*" /></div>
      <div class="form-group"><label>Data</label><input type="date" /></div>
      <div class="form-group"><label>Hora</label><input type="time" /></div>
      <button class="btn">Agendar Post</button>
    </div>

### Menu lateral - 📝 Agentes
- Agentes Inteligentes:
  - Agendamento IA Deixe que nossa IA decida em quais dias e horarios postar Botão “Abrir IA” estilizado Que leva a um modal estiloso para fazer o upload novos conteúdos:
    - Seleção da rede social
    - Campo de titulo 
    - Campo de descrições 
    - Upload de multiplos imagem ou vídeo
    - Escolha de data/hora (ia ira decidir)
    - Botão “Agendar Com IA” estilizado

  - Upload com IA Deixe que nossa IA decida Sugestões inteligentes para títulos e descrições  Botão “Abrir IA” estilizado Que leva a um modal estiloso para fazer o upload novos conteúdos:
    - Seleção da rede social
    - Campo de titulo (que a ia ira preencher)
    - Campo de descrições (que a ia ira preencher)
    - Upload de multiplos imagem ou vídeo
    - Escolha de data/hora
    - Botão “Upload Com IA” estilizado

### Menu lateral - 📝 Histórico de Posts Agendados
- Tabela elegante com:
  - Ícone da rede social
  - Resumo do texto
  - Data e hora agendadas
  - Status (agendado, enviado, erro) com cores distintas
  - Ações: editar, excluir, visualizar detalhes

### Menu lateral - ⚙️ Configurações da Conta
- Painel com:
  - Nome e e-mail do usuário
  - Rede Youtube com ícone e com Botão “Conectar nova conta” 
  - Rede Tiktok com ícone e com Botão “Conectar nova conta” 
  - Rede Twiter com ícone e com Botão “Conectar nova conta” 
  - Rede Instagram com ícone e com Botão “Conectar nova conta” 
  - Plano atual (ex: Gratuito, Pro)

