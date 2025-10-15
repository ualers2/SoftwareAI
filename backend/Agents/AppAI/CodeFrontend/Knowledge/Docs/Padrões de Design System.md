Padrões de Design System (DS) e Componentização de Alto Nível
Este documento eleva os componentes (já definidos em) a um Design System, fornecendo regras claras para a criação e uso de elementos de interface (UI/UX) consistentes.

1. Princípios Fundamentais do Design System (DS)
1.1. Fonte Única da Verdade Visual (Single Source of Truth)
ID: DS-VISUAL-SSOT
Palavras-Chave: design system single source of truth atomic design
Regra: Todos os elementos de UI (Cores, Fontes, Espaçamentos, Componentes) DEVEM ser definidos e importados de um local central. O time júnior e o Agente de IA NUNCA devem aplicar estilos diretamente nos componentes de Pages ou Hooks; eles devem sempre usar os componentes de UI de src/components/Common/ ou tokens do Tailwind.

1.2. Componentes Adaptáveis e Responsivos
ID: DS-RESPONSIVE-FIRST
Palavras-Chave: design system responsivo mobile first
Regra: O desenvolvimento DEVE ser Mobile First. Todos os componentes, por padrão, devem ser projetados e codificados para funcionar e parecerem excelentes em telas pequenas antes de serem adaptados para telas maiores (desktop). O uso de utilitários de responsividade do Tailwind CSS (ex: md:, lg:) é obrigatório.

1.3. Documentação de Componentes
ID: DS-COMPONENT-DOCS
Regra: Embora estejamos focados na velocidade, cada componente de UI não trivial (ex: Modal, Table, Card) DEVE ter um arquivo de documentação ou story adjacente (ex: usando Storybook ou um README simples no componente) descrevendo suas props e casos de uso.
Requisito para o Agente de IA: A IA deve gerar comentários no código-fonte do componente descrevendo suas funcionalidades.

2. Padrões de Componentização Específicos
2.1. Nomenclatura e Tipos de Componentes
ID: DS-COMPONENT-ATOMIC
Palavras-Chave: atomic design nomenclatura
Regra: Adotar a lógica do Atomic Design (Átomos, Moléculas, Organismos) para organizar a pasta src/components/

Nível	Exemplo de Pasta/Nome	Descrição	Onde Usar
Átomos	Button.tsx, Input.tsx	Elementos HTML puros e básicos, com pouco ou nenhum estado interno.	Em toda parte.
Moléculas	LoginForm.tsx, UserCard.tsx	Grupos de Átomos que funcionam juntos (ex: Input + Rótulo + Botão).	Dentro de Organismos ou Pages.
Organismos	Header.tsx, Sidebar.tsx	Seções complexas da interface (ex: um Header com navegação e busca).	Dentro de Pages.
2.2. Separação de Estilos (Tokens de Design)
ID: DS-STYLE-TOKENS
Regra: Todos os valores de estilo (cores, espaçamento, tamanhos de borda) DEVEM ser referenciados por meio de tokens definidos no arquivo de configuração do Tailwind (ou variáveis CSS se necessário) e NUNCA por valores literais.
Exemplo: Usar className="bg-primary-500" ao invés de style={{ backgroundColor: '#1A73E8' }}.

3. Padrões de Interação e Feedback (Avançado)
3.1. Feedback Visual de Interação
ID: DS-INTERACTION-FEEDBACK
Palavras-Chave: hover focus active
Regra: Todo elemento interativo (botões, links, ícones clicáveis) DEVE fornecer feedback visual claro para os estados de Hover, Focus (acessibilidade com teclado), e Active (clique). O Tailwind deve ser usado para definir estes estados.

3.2. Hierarquia Visual de Ações
ID: DS-ACTION-HIERARCHY
Palavras-Chave: botões primário secundário destrutivo
Regra: Botões e Ações devem ter uma hierarquia visual clara, geralmente usando apenas um Botão Primário (destacado, ex: cor principal) por tela/formulário, e os demais como Secundários (contorno/fundo claro) ou Destrutivos (cor de alerta/vermelha).

3.3. Uso de Cores Semânticas
ID: DS-SEMANTIC-COLOR
Regra: As cores DEVEM ser usadas de forma consistente para transmitir significado, NUNCA apenas por estética:

Primary (Azul/Verde): Ações Principais, Links.

Success (Verde): Confirmação, Operação Bem-Sucedida.

Warning (Amarelo): Atenção, Ações que Requerem Cuidado.

Danger (Vermelho): Erros, Ações Destrutivas ou Irreversíveis.