3. Padrões de Requisitos Simplificados
3.1. Template de Requisito Funcional (RF) - Básico
ID: TEMPLATE-RF-BASICO
Palavras-Chave: modelo requisito funcional basico
Foco em clareza e nos Passos de Teste para verificação manual.

Exemplo Modelo:
RF-XXX: [Módulo] - Título da Funcionalidade
Descrição (O que deve fazer): O usuário deve ser capaz de realizar o cadastro no sistema.
Regras de Negócio Chave:

O e-mail deve ser único no sistema (verificar no PostgreSQL).

A senha deve ter no mínimo 8 caracteres.

Após o cadastro, o usuário deve ser redirecionado para a página de login.
Passos de Teste (Para Estagiário):

[ ] Tentar cadastrar com um e-mail já existente. Esperar erro 400.

[ ] Cadastrar com senha de 6 caracteres. Esperar mensagem de erro.

[ ] Cadastrar com dados válidos. Verificar se o registro aparece na tabela usuarios do PostgreSQL.

3.2. Template de Requisito Não-Funcional (RNF) - Foco em Usabilidade/Segurança
ID: TEMPLATE-RNF-SIMPLES
Palavras-Chave: modelo requisito nao-funcional junior usabilidade
Os RNFs devem ser simples e diretamente relacionados à experiência do usuário ou à segurança básica.

Exemplo Modelo:
RNF-XXX: [Categoria: Usabilidade] - Mensagens de Erro
Especificação: Todas as mensagens de erro (validação de formulário ou API) DEVEM ser amigáveis e escritas em Português.
Justificativa: Garantir que o usuário entenda o problema e saiba como corrigi-lo.

RNF-YYY: [Categoria: Segurança] - Logs de Acesso
Especificação: Toda tentativa de login (sucesso ou falha) DEVE gerar um log (IP, timestamp, status) no MongoDB para fins de auditoria básica.
Justificativa: Rastrear atividades suspeitas.