🤖 Tornar 100% autônomo com OpenAI
Sim, é possível usar a API da OpenAI com Selenium para automatizar testes sem precisar informar manualmente os elementos. A ideia é gerar ações de interação com base no DOM da página.

🔁 Exemplo de abordagem:
Captura o document.body.innerHTML com Selenium.

Envia esse HTML bruto para o GPT-4 com um prompt do tipo:

"Acesse o input de email, digite 'usuario@teste.com', depois o campo de senha, digite '123456', clique no botão de login. Use seletores robustos (id, name ou text). Retorne apenas o código Python Selenium para isso."

Executa o código retornado dinamicamente via exec() ou grava em um script.

