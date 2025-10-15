Padrões de Interface e Experiência do Usuário (UI/UX)
Este documento estabelece as regras básicas de design e interação para garantir uma aplicação com excelente usabilidade para o time júnior. O foco é na consistência, clareza e na minimização da frustração do usuário.

1. Padrões de Formulários e Entradas
1.1. Estado de Feedback Imediato
ID: UX-FORM-FEEDBACK
Palavras-Chave: formulário feedback erro validação
Regra: A validação de campos (erros de formato, campos obrigatórios) DEVE ocorrer imediatamente (on-blur ou on-change) ANTES do envio para o Back-End (validação local no Front-End). O campo com erro DEVE ter sua borda destacada (ex: cor vermelha) e a mensagem de erro deve estar próxima ao campo.

1.2. Rótulos e Placeholder
ID: UI-FORM-LABELS
Palavras-Chave: formulário rótulo placeholder
Regra: Todo campo de entrada DEVE ter um rótulo (<label>) claro e visível acima do campo, mesmo que o placeholder seja usado como dica. O placeholder NUNCA deve substituir o rótulo.

1.3. Acessibilidade (Foco em Teclado)
ID: UX-FORM-ACCESSIBILITY
Palavras-Chave: acessibilidade teclado tab
Regra: A navegação entre os campos do formulário DEVE ser sequencial e funcional usando a tecla TAB. Todos os botões e links navegáveis devem receber foco (focus state) visualmente claro.

2. Padrões de Carregamento e Estados Vazios
2.1. Indicadores de Carregamento (Loading States)
ID: UX-LOADING-INDICATOR
Palavras-Chave: loading skeleton spinner
Regra: Para chamadas de API que demoram mais de 500ms, NÃO deve ser exibido um spinner genérico. Em vez disso, DEVE ser usado um Skeleton Loader (um desenho da estrutura da interface que está por vir) no local exato do conteúdo, para otimizar a percepção de velocidade.

2.2. Estados Vazios (Empty States)
ID: UI-EMPTY-STATE
Palavras-Chave: lista vazia estado
Regra: Quando uma lista ou tabela não contém dados (ex: uma busca sem resultados, carrinho vazio), o componente NÃO deve ficar simplesmente em branco. DEVE ser exibida uma mensagem amigável e uma ilustração ou ícone, sugerindo ao usuário qual ação tomar para preencher a tela (ex: "Nenhum pedido encontrado. Que tal fazer um novo pedido?").

2.3. Transição de Carregamento
ID: UI-LOADING-TRANSITION
Regra: A transição de um estado de carregamento para o conteúdo final DEVE ser suave, evitando o "flash" ou layout shift (mudança abrupta de layout) após a renderização do dado.

3. Padrões de Navegação e Arquitetura da Informação
3.1. Consistência do Header/Sidebar
ID: UI-NAV-CONSISTENCY
Palavras-Chave: navegação header sidebar
Regra: O componente de Header (cabeçalho) e/ou Sidebar (barra lateral) DEVE permanecer inalterado e visível em todas as rotas (exceto nas páginas de Login/Erro). A estrutura da navegação NÃO DEVE mudar de módulo para módulo, exceto pela indicação visual da rota ativa.

3.2. Feedback de Ação (Toasts/Notificações)
ID: UX-ACTION-FEEDBACK
Palavras-Chave: toast notificação feedback de sucesso
Regra: Toda ação destrutiva (ex: exclusão) ou crítica (ex: cadastro/edição) DEVE gerar um feedback visual não-intrusivo (ex: um Toast temporário no canto da tela) indicando sucesso ou falha, com a mensagem amigável vinda do Back-End.

3.3. Confirmação de Ações Críticas
ID: UX-CRITICAL-CONFIRMATION
Palavras-Chave: modal confirmação exclusão
Regra: Antes de executar qualquer ação destrutiva ou irreversível (ex: excluir um usuário, cancelar um pedido), o sistema DEVE apresentar um Modal de Confirmação pedindo que o usuário confirme a intenção, com botões de ação claramente rotulados (ex: "Sim, Excluir" em vermelho e "Cancelar").

4. Padrões de Componentização e Design System
4.1. Fonte Única da Verdade para Componentes
ID: UI-SINGLE-SOURCE-COMPONENT
Palavras-Chave: design system typescript props
Regra: Componentes como Button, Input e Modal DEVEM ser definidos e tipados apenas uma vez em src/components/Common/. A regra é NUNCA reescrever o mesmo componente em outra parte da aplicação.

4.2. Uso de Ícones
ID: UI-ICON-USAGE
Palavras-Chave: ícones
Regra: Ícones DEVEM ser usados para reforçar a semântica da ação ou do conteúdo, mas NUNCA devem ser o único elemento de comunicação. O texto adjacente é obrigatório (ex: botão de "Salvar" com ícone de disquete, não apenas o ícone).

4.3. Consistência de Tipografia e Cores
ID: UI-STYLE-CONSISTENCY
Palavras-Chave: tailwind cores tipografia
Regra: Todas as cores, espaçamentos e tamanhos de fonte DEVEM ser baseados em tokens definidos no Tailwind CSS ou na biblioteca de Design System. O uso de valores hexadecimais ou píxeis hard-coded no CSS é PROIBIDO.