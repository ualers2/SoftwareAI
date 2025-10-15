Padrões de Convenção e Estrutura de Código (Front-End)
Este documento mapeia a estrutura de pastas do Front-End para as responsabilidades do código, garantindo que o time júnior saiba onde colocar cada tipo de lógica.

1. Mapeamento da Estrutura de Módulos (Separation of Concerns)
A estrutura de Front-End/src implementa o padrão de Camadas de Apresentação (Presentation Layer), separando as preocupações:

Pasta	Responsabilidade	Descrição	Padrões de Uso (ID RAG)
pages	View Principal (Controller/Coordinator)	Contém os componentes principais (ex: Login.tsx, Dashboard.tsx). Sua única responsabilidade é coordenar o estado global, chamar hooks e renderizar os componentes de UI. NUNCA deve conter lógica de formatação ou acesso direto à API.	ARQ-SPA-SIMPLES
components	Componentes de UI (View)	Blocos de construção reutilizáveis (ex: Button, Card, Header). Devem ser puros (stateless) e receber dados via props.	ARQ-SPA-SIMPLES, CODE-REACT-PURE-COMPONENTS
hooks	Lógica de Dados/Estado (Service)	Lógica reusável para manipular o estado local ou chamar a API. Ex: useAuth(), useUserData(). É o ponto de contato entre a Page e a camada de Lib.	CODE-REACT-HOOKS, FRONT-API-COMMUNICATION
lib	Funções Utilitárias/API	Código sem estado, reutilizável (ex: formatDate(), calculateTax()) e o cliente HTTP configurado. Ex: apiClient.ts.	FRONT-API-COMMUNICATION, FRONT-API-ERROR-HANDLE
contexts	Estado Global	Mecanismo para gerenciar o estado global da aplicação (ex: Tema, Usuário Autenticado) sem prop-drilling.	-
constants	Constantes Globais	Variáveis que não mudam (ex: URLs de API, textos estáticos).	-

Padrões de Código Essenciais (Front-End)
1. Padrão de Componentes React

1.1. Componentes Puros e Tipagem (TypeScript)
ID: CODE-REACT-PURE-COMPONENTS
Palavras-Chave: react typescript componentes puros props
Regra: A maioria dos componentes em src/components DEVE ser funcional e pura (stateless), aceitando as propriedades (props) e emitindo eventos se necessário. Toda prop DEVE ser explicitamente tipada com interface ou type do TypeScript.

1.2. Evitar Lógica de Negócio em Componentes (Separação de Preocupações)
ID: CODE-REACT-NO-BUSINESS-LOGIC
Regra: Componentes em src/components NÃO DEVEM conter lógica de negócio complexa, chamadas de API diretas (fetch ou axios dentro do componente), ou manipulação de estado que não seja puramente de UI. Delegar isso aos Hooks e Pages.

2. Padrões de Hooks e Estado

2.1. Hooks para Lógica de Dados
ID: CODE-REACT-HOOKS
Palavras-Chave: react hooks usememo usecallback
Regra: Utilizar Hooks customizados em src/hooks para isolar a lógica de acesso a dados, manipulação de estado complexa ou efeitos colaterais (useEffect). Isso torna a lógica reutilizável e mais fácil de testar.

2.2. Otimização de Performance (Básica)
ID: CODE-REACT-PERFORMANCE-JUNIOR
Regra: Usar useMemo para memorizar cálculos caros e useCallback para memorizar funções que são passadas como props para componentes filhos, evitando re-renderizações desnecessárias.

3. Padrão de Comunicação com a API (Ver documento de Comunicação)
Regra: A comunicação deve ser centralizada em lib/apiClient.ts e consumida pelos Hooks.