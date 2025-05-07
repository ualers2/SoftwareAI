
## 🧠 Instrução para o Agente de Code Review Timeline Agent
**Objetivo:**  
Validar se os arquivos html listados abaixo estao presentes se nao tiver validado encaminhar ao agente especifico
- {doc_md}/cronograma.md
Encaminhe para o agente correto com base na secao `## 🌐 Agente de cada arquivo:` 

---

## 🔍 Etapas obrigatórias antes da codificação
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo {doc_md}/cronograma.md para que seja possivel analisar se o arquivo existe
autogetlocalfilecontent:
- preferred_name: "cronograma.md"
- fallback_names: ["cronograma.md"]
- search_dir: {doc_md}

## 🌐 Agente de cada arquivo:

- cronograma.md\n
se o arquivo existir retorne "ok, validado" e NAO encaminhe o usuario
se o arquivo nao existir ler o arquivo {doc_md}/preplanejamento.md com autogetlocalfilecontent e Encaminhar o usuário junto ao conteudo completo de {doc_md}/preplanejamento.md para o agente code_requirements_and_timeline_agent com o Handoffs transfer_to_code_requirements_and_timeline_agent
\n

    