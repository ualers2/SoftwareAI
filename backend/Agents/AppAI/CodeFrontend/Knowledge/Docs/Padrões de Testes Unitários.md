Padrões de Testes Unitários (Front-End React)
Garantir que os juniores saibam como testar a UI e a lógica isoladamente.

2.1. Ferramenta de Teste
ID: TEST-FE-TOOL
Palavras-Chave: testes frontend unitarios jest rtl
Regra: Utilizar Vitest como runner de testes e React Testing Library (RTL) como biblioteca principal para testes de componentes. Foco em testar o comportamento (o que o usuário vê) e não os detalhes de implementação do React.

2.2. Testes para a Camada de Componentes (UI)
ID: TEST-FE-UI-COMPONENT
Palavras-Chave: testes componentes react rtl mock
Regra: Ao testar um componente em src/components/, é OBRIGATÓRIO utilizar mocking para simular funções passadas como props ou context (se aplicável). O teste deve verificar se o componente renderiza corretamente com as props fornecidas e se o evento correto é disparado (ex: fireEvent.click).

2.3. Testes para a Camada de Lógica (Hooks/Lib)
ID: TEST-FE-LOGIC-HOOKS
Palavras-Chave: testes hooks lógica reativa
Regra: Testes de Hooks customizados devem usar a função renderHook do RTL (ou similar) para garantir que a lógica de estado e side effects esteja correta. O acesso à API (apiClient) DEVE ser mockado para que o teste seja unitário, verificando apenas o fluxo de sucesso/erro do hook.

2.4. Localização dos Testes
ID: TEST-FE-LOCATION
Regra: Todos os arquivos de teste devem residir na mesma pasta que o código que está sendo testado (ex: src/components/Button.test.tsx) ou em uma pasta __tests__ adjacente, e ter o sufixo .test.tsx ou .test.ts.