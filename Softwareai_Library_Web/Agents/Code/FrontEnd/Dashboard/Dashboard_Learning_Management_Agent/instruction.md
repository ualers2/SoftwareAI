## 🧠 Instrução Profissional para Geração da Área do Usuário (Painel de Controle)

### Agente: Code Front End Dashboard Learning Management Agent

## 🎯 Objetivo

Gerar um **único arquivo `{path_html}/dashboard.html`** contendo um painel de controle orientado à **Gestão de Cursos e Alunos**, com as seguintes funcionalidades:

- **Progresso em módulos**: visualização clara do andamento de cada aluno em cada módulo do curso.
- **Taxas de conclusão**: indicadores de porcentagem de alunos que concluíram módulos e cursos inteiros.
- **Engajamento por vídeo/aula**: métricas de tempo assistido, número de reproduções e interações (curtidas, comentários).
- **Avaliações**: listagem de notas médias por aluno e por curso, com histogramas rápidos.
- **Certificações emitidas**: contagem e lista de certificados gerados, com opção de download.

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

⚠️ O painel deve refletir exatamente os recursos anunciados em `index.html` para cursos e alunos.

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

### 🧩 Menu Lateral - 📚 Cursos e Alunos
Ao clicar em **Cursos e Alunos**, deve aparecer:

- **Visão Geral de Cursos**:
  - Cards com cada curso ativo, mostrando:
    - 📛 Nome do curso
    - 📊 Progresso médio (%) de conclusão
    - 👥 Total de alunos inscritos
    - 🧠 Botão para ver detalhes do curso
- **Progresso por Módulo**:
  - Gráfico de barras simples (JS puro + Canvas/SVG) mostrando módulos e porcentagem concluída.
- **Lista de Alunos**:
  - Tabela com:
    - 👤 Nome do aluno
    - 🕒 Progresso atual (% e módulo)
    - ⭐ Nota média
    - 🎖️ Status da certificação (emitida / pendente)
    - 🔍 Botão “Ver Perfil”

### 🧩 Menu Lateral - ▶️ Engajamento em Vídeo/Aula
Ao clicar em **Engajamento**, deve aparecer:

- **Métricas por Aula**:
  - Tabela ou lista com:
    - ▶️ Título da aula
    - ⏱️ Tempo médio assistido
    - 🔁 Taxa de replay (%)
    - 💬 Número de comentários
    - 👍 Curtidas
- **Visão Rápida**:
  - Cards com as 3 aulas mais engajadas e 3 menos engajadas.

### 🧩 Menu Lateral - 📝 Avaliações e Certificações
Ao clicar em **Avaliações**, deve aparecer:

- **Histograma de Notas**:
  - Gráfico simples mostrando distribuição de notas.
- **Tabela de Avaliações**:
  - Aluno | Curso | Nota | Data da Avaliação | Detalhes (Modal)
- **Certificações Emitidas**:
  - Lista com:
    - 🏷️ Nome do certificado
    - 👤 Aluno beneficiado
    - 📅 Data de emissão
    - 📥 Botão de download do certificado (PDF)

### 🧩 Menu Lateral - ⚙️ Configurações do Painel
Ao clicar em **Configurações**, deve aparecer:

- **Opções de Exibição**:
  - Alternar tema claro/escuro manualmente
  - Ajustar intervalos de atualização automática de dados
- **Gerenciamento de Usuários**:
  - Adicionar/remover admins
  - Definir permissões por perfil

---

## 🔑 Regras Essenciais

✅ **Único arquivo**: HTML, CSS e JS sem dependências externas.
✅ **Responsividade** e **acessibilidade** garantidas.
✅ **Design fiel** à landing page.
✅ **Sem inline styles** e **sem atributos `onclick`**.
✅ **Código limpo** e bem comentado.

---
