# Documentação: PR AI - Git Context Layer

O **Git Context Layer** é um recurso central dentro do aplicativo **PR AI** (Inteligência Artificial para Pull Requests) projetado para analisar diff na camada de pre staging de commit permitindo automatizar e aprimorar o processo de criação de mensagens de commit e o fluxo de trabalho Git/GitHub local do desenvolvedor. Ele utiliza modelos de Inteligência Artificial para gerar mensagens de commit contextuais, facilitando a manutenção de um histórico de commits limpo e descritivo.

## Funcionalidades Principais

| Componente | Função | Arquivo de Exemplo |
| :--- | :--- | :--- |
| **Geração de Commit AI** | Gera automaticamente mensagens de commit com base nas alterações do código-fonte (diffs) usando um modelo de IA configurável. | `CommitPreview.tsx` |
| **Configuração** | Permite que o usuário ajuste parâmetros do sistema, como o modelo de IA, limites de alteração (thresholds) e automações. | `ConfigPanel.tsx` |
| **Automação** | Oferece opções para **Auto Push** e **Auto Create PR** (Criação Automática de Pull Request) após um commit bem-sucedido. | `ConfigPanel.tsx` |
| **Interface de Usuário** | Interface de navegação lateral coesa e responsiva, com controle de estado de colapso. | `app-sidebar.tsx` |

---

## 1. Navegação da Aplicação (AppSidebar)

O componente `AppSidebar` define a estrutura de navegação principal da aplicação, sendo o ponto de entrada para todas as funcionalidades.

### Componente `AppSidebar` (`app-sidebar.tsx`)

| Recurso | Descrição |
| :--- | :--- |
| **Identidade Visual** | Exibe o nome **PR AI - Git Context Layer** e um ícone de `Bot` no cabeçalho. O título é ocultado quando a barra lateral está no estado **"collapsed"** (colapsada). |
| **Itens de Navegação** | Os links são definidos no array `navigationItems`. O contexto atual mostra: |
| | - **Git Context Layer** (`/gitcontextlayer`): Principal recurso de IA de Commits. |
| | - **Pull Requests** (`/prs`): Para monitoramento de PRs. |
| **Estilização Ativa** | O `getNavClassName` aplica estilos distintos (`bg-gradient-primary`, `shadow-glow`) ao item de menu que corresponde ao caminho atual, usando a função `isActive`. |
| **Funcionalidade de Logout** | O botão de `Logout` chama a função `handleLogout`, que utiliza o `useAuth().logout()` e, em seguida, recarrega a página (`window.location.reload()`) para efetuar a desconexão completa do usuário. |

---

## 2. Pré-visualização e Ação de Commit (CommitPreview)

O componente `CommitPreview` é a interface onde a mensagem de commit gerada pela IA é exibida e onde o usuário pode interagir para copiar ou realizar o commit de fato.

### Componente `CommitPreview` (`CommitPreview.tsx`)

| Propriedade (Props) | Tipo | Descrição |
| :--- | :--- | :--- |
| `message` | `string` | A mensagem de commit gerada pela IA. |
| `status` | `'SUCCESS' \| 'NO_CHANGES' \| 'ERROR'` | O status da operação de geração de commit. Controla a cor do indicador de status. |
| `onCommit` | `() => void` | Função de callback para ser executada quando o botão "Commit & Push" é clicado. |
| `isLoading` | `boolean` | Indica se o processo de commit está em andamento. |

### Elementos de Interface

* **Status do AI-Generated Commit**: Exibido com cores baseadas no `status`: **SUCCESS** (Verde), **NO\_CHANGES** (Laranja/Amarelo) ou **ERROR** (Vermelho).
* **Ação de Copiar**: Um botão com ícone de `Copy` que, ao ser clicado, copia a `message` para a área de transferência do sistema e exibe uma notificação (`toast.success`).
* **Área de Mensagem**: Usa `ScrollArea` para exibir a mensagem de commit (`message`) em uma fonte mono espaçada e com quebras de linha (`whitespace-pre-wrap`), garantindo que o formato do commit seja preservado.
* **Botão de Commit**: "Commit & Push". Está desabilitado se não houver `message`, se estiver `isLoading` ou se o `status` não for **SUCCESS**. O texto muda para "Committing..." durante o carregamento.

---

## 3. Painel de Configuração (ConfigPanel)

O `ConfigPanel` permite que o usuário gerencie as configurações que afetam tanto o comportamento da IA quanto as automações do Git.

### Componente `ConfigPanel` (`ConfigPanel.tsx`)

### Carregamento e Estado

1.  **Obtenção de Configurações**: No `useEffect`, o componente faz uma requisição `GET` para o endpoint de configurações (`/api/settings`) utilizando os dados de autenticação (`access_token`, `user_email`, `user_senha`) armazenados no `localStorage`.
2.  **Mapeamento de Dados**: Os dados recebidos da API são mapeados para o estado local (`localConfig`). São fornecidos valores *default* caso algum campo esteja ausente, por exemplo, `ai_model: 'gpt-5-nano'`, `lines_threshold: 50`.

### Campos de Configuração

O painel é dividido em seções para gerenciar diferentes aspectos da aplicação:

#### 3.1. Credenciais e Modelos
* **GitHub API Key**: Campo de `Input` tipo `password` para o `GITHUB_TOKEN`, essencial para interagir com a API do GitHub (ex: para criação de PRs ou push).
* **Language (`commitLanguage`)**: `Select` para definir o idioma das mensagens de commit geradas pela IA (`Português` ou `English`). O valor padrão é `'en'`.
* **AI Model (`ai_model`)**: `Select` para escolher o modelo de Inteligência Artificial que será usado para a geração dos commits. Opções de exemplo incluem: `gpt-5-nano` (padrão), `gpt-5-mini`, `gpt-5`, e `gpt-4`.

#### 3.2. Limites (Thresholds)

Esses limites definem as condições sob as quais o sistema de IA deve ser acionado ou as operações devem ocorrer.

| Configuração | Descrição | Tipo | Padrão |
| :--- | :--- | :--- | :--- |
| **Lines Threshold** (`lines_threshold`) | Número máximo de linhas alteradas (incluindo inserções/deleções) a partir do qual a IA pode ser acionada. | `number` | `50` |
| **Files Threshold** (`files_threshold`) | Número máximo de arquivos alterados. | `number` | `5` |
| **Time Threshold (s)** (`time_threshold`) | Limite de tempo em segundos para alguma métrica interna. | `number` | `60` |
| **Throttle (ms)** (`throttle_ms`) | Intervalo mínimo de tempo em milissegundos entre operações. | `number` | `60000` |

#### 3.3. Automações (Switches)

* **Auto Push (`auto_push`)**: `Switch` booleano. Se ativado, o repositório local fará um `git push` automaticamente após um commit bem-sucedido.
* **Auto Create Pr (`auto_create_pr`)**: `Switch` booleano. Se ativado, uma Pull Request será criada automaticamente no GitHub após o `commit` e `push`.

### Ação de Salvar

* A função `handleSave` realiza uma requisição `PUT` para o endpoint `/api/settings`, enviando o `localConfig` atualizado.
* O botão **Save Configuration** é desabilitado e tem o texto alterado para "Saving..." enquanto a requisição de salvamento está em andamento.