
**🧠 Objetivos:**  
- Criar, Salvar e incluir no Pull Request `navigation.js` – JavaScript modular e limpo para lidar com navegação via clique (deve ser adicionado no fim do html {path_html}/index.html antes de </body> deve ser adicionado <script src="{path_js}/navigation.js"></script> )
- Modificar, Salvar e incluir no Pull Request `index.html` – REMOVER (retirar excluir nao melhorias nem alteracoes apenas exclua) as referencias de `href` dos botoes de planos para que seja compativel com a logica de {path_html}/navigation.js
- Modificar, Salvar e incluir no Pull Request `index.html` – Refatore o javascript que esta dentro de script (<script codigo js </script>) e coloque ele em um novo arquivo chamado {path_js}/landing.js depois de refatorado para o arquivo adicione antes de </body> <script src="{path_js}/landing.js"></script>

---

### 📁 Localização Esperada dos Arquivos
- `{path_js}/navigation.js`
- `{path_js}/landing.js`
- `{path_html}/index.html`

### 📁 Localização Esperada dos Arquivos navigation.js, landing.js e index.html
### 📥 autosave
- **path:** `{path_js}/navigation.js`
- **code:** conteúdo completo gerado de navigation.js
### 📥 autosave
- **path:** `{path_js}/landing.js`
- **code:** conteúdo completo gerado de landing.js
### 📥 autosave
- **path:** `{path_html}/index.html`
- **code:** conteúdo completo gerado de index.html

---

## 🔍 Etapas obrigatórias antes da codificação
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo index para que seja possivel o desenvolvimento das modificacoes
autogetlocalfilecontent:
- preferred_name: "index.html"
- fallback_names: ["index.html"]
- search_dir: {path_html}

---

## 🔧 Regras técnicas
- Utilizar **JavaScript puro**, sem bibliotecas externas
- O script JS deve ser modular e organizado, com funções nomeadas
- Os botões devem ser localizados preferencialmente por `id`, ou por `class` se necessário
- As ações de redirecionamento podem ser feitas via:
- `window.location.href = "..."`
- Garantir que qualquer JS seja executado após `DOMContentLoaded`
- Incluir mensagens de erro claras no console se elementos não forem encontrados
- Código funcional e legível
- Redirecionamento correto dos botões
- **Sem uso de `onclick` direto no HTML**
- Toda alteração em arquivos deve ser salva e incluída no PR
- jamais (Não) crie codigos genericos e sem utilidades exemplo "// JavaScript específico da página de destino pode ser adicionado aqui" ou "// Melhorias futuras para a landing page podem ser adicionadas neste arquivo."
- jamais (Não) modifique arquivos que nao estao na secao "**Objetivo:**  "
- jamais (Não) modifique arquivos se for para retirar logicas ja existentes (que nao foram solicitadas as mudanças em "**Objetivo:**  ")

