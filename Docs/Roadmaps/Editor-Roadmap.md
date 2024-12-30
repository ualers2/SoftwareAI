## 📖 Editor Roadmap
- [X] `Editor keys github` create a section for editing agent keys on github
- [X] `Editor open ai` create a section for editing open ai keys
- [X] `Editor Firebase` create a section for editing firebase app keys
- [] `Editor Categoria` Criar seção de criação de categoria
- []  Criar codigo para adicionar agente buildado em `_init_agents_`
- []  Criar codigo para Armazenar os chat completions com store
- []  Criar Opcao para adicionar mais de uma function ao buildar agente
- []  Criar Opcao para selecionar argumentos para chamada do agente ja conhecidos e consolidados
- []  Criar Opcao para buildar agentes especificos ja consolidados com 1 click como por exemplo `CloudArchitect` que cria documentos .md de alta qualidade ou `QuantumCore` que é capaz de criar um software e upalo no github
- []  Seção para remover agentes 
- []  Seção para remover chaves da open ai
- []  Seção para remover chaves do firebase
- []  Seção para remover chaves do github



## **Editor**  
- **22/12/2024**  
  - [] `22:30:00` QCustomCodeEditor so that modifications can be made directly to the agent code


- **Editor instructions**  
  - [X] Functional Instruction Editor 
  - [X] Functional Instruction Creator 

- **Agent creator**  
  - [X] Advanced vector storage when selected, each file argument is uploaded to the vector store and attached to the agent significantly reducing input token costs
  - [X] Github key selector for the agent, this means that the selected key will be used in building and using the agent
  - [X] openAI key picker for the agent, this means that the selected key will be used by the agent
  - [X] Distillation configuration it is possible to select the Distillation of Agent inputs and outputs it is possible to save in 2 formats the first is a json with only input and output the second is the finetunning jsonl format that follows the standards provided by openai ` {"messages": [{"role": "system", "content": "Marv"}, {"role": "user", "content": "France"}, {"role": "assistant", "content": "Paris"}]}`
  - [X] Completions distillation configuration, some agents are better off using completions to generate basic things like `a description for a github repository`, you may want to do this with the agent itself but when attaching files to the agent it is not It is possible to change the response format to json, you can structure an output if you prefer. use completions to avoid problems
  - [X]
  - [X] Key In Firebase
  - [X] Name Agent
  - [X] Agent Category
  - [X] Instruction Settings
  - [X] Instruction Settings/InstructionAgentCreate
  - [X] Instruction Settings/AditionalInstructionsAgentCreate
  - [X] Functions Settings
  - [X] Functions Settings/AgentTools
  - [X] Functions Settings/namefunction_agentcreate
  - [X] Functions Settings/FunctionPython
  - [X] Functions Settings/FunctionPythonOutput
  - [X] Prompt Settings
  - [X] Prompt Settings/Promptmain
  - [X] Prompt Settings/PromptRules
  - [X] Prompt Settings/PromptExample
  - [X] Advanced Vectorstore
  - [X] Arguments Settings
  - [X] Arguments Settings/Args to call agent
  - [X] Arguments Settings/the Args will be of the typew
  - [X] Upload Vectorstore No Agente
  - [X] Upload Vectorstore Na Thread
  - [X] Upload File Na Thread
  - [X] Upload File Na Mensagem
  - [X] Upload imagem para visao Na Thread
  - [X] Upload lista de arquivos para code interpreter Na Thread
  - [X] Upload lista de arquivos No Agente


