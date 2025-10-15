Padrões de Mocking e Desenvolvimento Desacoplado (Front-End)
Este documento estabelece as regras para simular a API do Back-End no Front-End, permitindo que o desenvolvimento da interface e da experiência do usuário (UI/UX) ocorra em paralelo e seja validado rapidamente.

1. Padrão de Contrato e Tipagem da API
1.1. Definição do Contrato da API (TypeScript Types)
ID: MOCK-CONTRACT-TYPES
Palavras-Chave: contrato api typescript interface mocking
Regra: Toda requisição e resposta de API DEVE ser primeiro definida em TypeScript Interfaces/Types em src/types/api.ts. Esta tipagem serve como o Contrato Oficial da API. O Front-End e o Back-End devem aderir a este contrato.
Exemplo: Antes de fazer a chamada, defina interface User { id: number; name: string; email: string; }.

1.2. Mapeamento de Tipagem para Dados Mockados
ID: MOCK-DATA-STRUCTURE
Regra: Todos os dados mockados (simulados) DEVEM ser gerados de forma que correspondam exatamente às TypeScript Interfaces. Isso garante que, quando o Back-End real for conectado, não haja erros de tipagem no Front-End.

2. Padrões de Simulação (Mocking)
2.1. Centralização do Mocking
ID: MOCK-TOOL-CENTRALIZATION
Palavras-Chave: mocking centralizado msw json-server
Regra: O Mocking de todas as rotas da API DEVE ser implementado em um módulo centralizado (ex: usando uma biblioteca como MSW - Mock Service Worker ou um serviço local simples em src/lib/mockApi.ts).

2.2. Uso Obrigatório do Mocking no Desenvolvimento Local
ID: MOCK-ENV-DEV
Palavras-Chave: ambiente desenvolvimento mocking
Regra: Durante o desenvolvimento local (npm run dev), o Front-End DEVE consumir os dados mockados por padrão (lido de uma variável de ambiente como VITE_USE_MOCKING=true).
Justificativa: Isso permite que a IA gere a interface e o time júnior veja e valide a UI/UX imediatamente.

2.3. Estrutura de Resposta Mockada (Padrão JSON)
ID: MOCK-RESPONSE-FORMAT
Regra: Os mocks de sucesso DEVEM retornar a resposta no formato JSON de sucesso definido (ID: CODE-API-SUCCESS), e os mocks de erro DEVEM retornar no formato de erro (ID: CODE-API-ERROR-HANDLING).
Exemplo de Mock de Sucesso (para uma lista de usuários):

TypeScript

{
  status: 'success',
  message: 'Dados mockados com sucesso.',
  data: [{ id: 1, name: 'Usuário Mock 1' }, { id: 2, name: 'Usuário Mock 2' }]
}
3. Integração com o Workflow de Aprovação
3.1. Chave de Toggle para Mocking
ID: MOCK-TOGGLE-KEY
Palavras-Chave: chave toggle mock
Regra: Deve haver uma chave de ambiente (ex: VITE_API_BASE_URL ou VITE_USE_MOCKING) que possa ser facilmente alternada para mudar o Front-End de Mock (Desenvolvimento/Aprovação Rápida) para API Real (Testes de Integração).
Requisito para Juniores: O Front-End gerado DEVE funcionar perfeitamente em ambos os modos, sem alterações no código dos componentes ou hooks.

3.2. Mocks de Erro para UI/UX
ID: MOCK-ERROR-SIMULATION
Palavras-Chave: simulação de erro ui ux
Regra: O time Front-End DEVE criar mocks específicos para simular os erros de API mais comuns (400, 401, 500) para garantir que os estados de erro da UI/UX (ex: Toast de falha, redirecionamento para Login, mensagens de formulário) sejam exibidos corretamente e sejam amigáveis.