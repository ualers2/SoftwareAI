Padrões de Arquitetura Simplificada (Front-End)
0. Padrões de Arquitetura Simplificada
Arquitetura Padrão: SPA Simples (Vite/React)
ID: ARQ-SPA-SIMPLES
Palavras-Chave: arquitetura spa simples react componentes
Padrão: Adotar o padrão de Componentes (Pages -> Components -> Hooks/Lib) para organizar a interface.
Fluxo: A Page (View) coordena a aplicação (ex: carrega dados), chamando Hooks (Service) para a lógica de dados, que, por sua vez, usa a camada de Lib (Communication/API) para interagir com o Back-End.
Vantagem: É altamente modular, fácil de testar isoladamente e é a arquitetura inicial mais recomendada para aprender a base de React.

2. Convenções de Nomenclatura e Arquivos
2.1. Nomenclatura de Arquivos
ID: CONV-FILE-NAMING-FE
Regra: Usar PascalCase para componentes React e camelCase para hooks e arquivos utilitários/lib. Extensão .tsx para componentes e .ts para lógica pura.
Bom: UserProfileCard.tsx, useFetchData.ts, apiClient.ts
Ruim: user_profile_card.tsx, usefetchdata.ts

2.2. Nomenclatura de Funções/Hooks
ID: CONV-FUNC-NAMING-FE
Regra: Hooks customizados devem começar com use (ex: useUser()). Funções em Libs devem usar verbos no infinitivo para indicar a ação que realizam (ex: formatDate, getAuthToken).

2.3. Uso de try...catch (Comunicação API)
ID: CONV-TRY-CATCH-FE
Regra: O bloco try...catch para chamadas de API (e tratamento de erro HTTP) DEVE ser usado na camada de Hooks (Service). A camada de Pages deve apenas receber a exceção tratada (ex: um erro amigável já formatado) para exibição.

3. Arquitetura Desejável (Front-End)

nomedoprojeto/
├── Front-End/
│   ├── ... (arquivos de config do Front-End como package.json, vite.config.ts)
│   └── src/
│       ├── components/
│       │   ├── Common/
│       │   │   ├── Button.tsx
│       │   │   ├── ...
│       │   ├── Forms/
│       │   │   ├── LoginForm.tsx
│       │   │   ├── ...
│       ├── constants/
│       │   ├── apiUrls.ts
│       │   ├── ...
│       ├── contexts/
│       │   ├── AuthContext.tsx
│       │   ├── ...
│       ├── hooks/
│       │   ├── useAuth.ts
│       │   ├── useProductList.ts
│       │   ├── ...
│       ├── lib/
│       │   ├── apiClient.ts  // Cliente HTTP configurado
│       │   ├── typeguards.ts
│       │   ├── formatDate.ts
│       │   ├── ...
│       ├── pages/
│       │   ├── Login.tsx
│       │   ├── Dashboard.tsx
│       │   ├── ...
│       ├── types/
│       │   ├── api.ts
│       │   ├── models.ts
│       │   ├── ...
│       ├── App.tsx
│       └── main.tsx
