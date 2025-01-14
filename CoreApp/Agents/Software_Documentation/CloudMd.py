from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import time
import re
import os

def extrair_codigo(texto):
    padrao = r'```python\n(.*?)\n```'  # Expressão regular para capturar código entre as tags
    resultado = re.search(padrao, texto, re.DOTALL)  # re.DOTALL permite que o "." capture quebras de linha
    if resultado:
        return resultado.group(1)  # Retorna o código encontrado
    return None


def GenDocsMdInGPU(
    mensagem,
    model_name = "Qwen/Qwen2.5-Coder-1.5B-Instruct", #"Qwen/Qwen2.5-Coder-3B-Instruct"#"Qwen/Qwen2.5-Coder-0.5B-Instruct"#
    cache_dir = "D:\LLMModels",
    max_new_tokens=2900
    ):

    start_time = time.perf_counter()

    instruction = '''

    ## Objectives
    Create comprehensive and high-quality technical documentation from Python source code, transforming comments, docstrings, and code into a structured and readable Markdown document.

    ### 1. Structure Example

    ```markdown
    # Module Title

    ## Overview
    Detailed description...

    ## Installation
    Installation instructions...

    ## Usage
    Usage examples...
    ```


    ### 2. Rules 
        #### 4.1 Headers
        - Use `#` for titles and subtitles
        - Clear and consistent hierarchy
        - Maximum of 3 depth levels

        #### 4.2 Code Blocks
        - Use triple backticks with language identification
        - Example: 
        ````markdown
        ```python
        def example():
            return "code"
        ```
        ````

        #### 4.3 Emphasis
        - *Italics* for technical terms
        - **Bold** for important highlights
        - `Inline code` for code references


    '''

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype="auto",
        device_map="auto",
        cache_dir=cache_dir
        
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name,cache_dir=cache_dir)

    messages = [
        {"role": "system", "content": f"{instruction}"},
        {"role": "user", "content": f"Create comprehensive and high-quality technical documentation from Python source code: {mensagem}"}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=max_new_tokens
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]



    end_time = time.perf_counter()
    print(end_time - start_time)
    #print(response)
    # docstring = extrair_codigo(response) 
    # print(docstring)
    # docstring = extrair_docstring(docstring)
    return response


# tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct", trust_remote_code=True)
# model = AutoModelForCausalLM.from_pretrained("deepseek-ai/deepseek-coder-1.3b-instruct", trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()
# messages=[
#     { 'role': 'user', 'content': f'{content_}'}
# ]
# inputs = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt").to(model.device)
# # tokenizer.eos_token_id is the id of <|EOT|> token
# outputs = model.generate(inputs, max_new_tokens=512, do_sample=False, top_k=50, top_p=0.95, num_return_sequences=1, eos_token_id=tokenizer.eos_token_id)
# response = tokenizer.decode(outputs[0][len(inputs[0]):], skip_special_tokens=True)
import shutil
#########################################
# IMPORT SoftwareAI Core
from softwareai.CoreApp._init_core_ import * 
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################
# IMPORT SoftwareAI All Paths 
from softwareai.CoreApp._init_paths_ import *
#########################################
# IMPORT SoftwareAI Instructions
from softwareai.CoreApp.SoftwareAI.Instructions._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp.SoftwareAI.Tools._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################
    

key_openai = OpenAIKeysteste.keys()
name_app = "appx"
appfb = FirebaseKeysinit._init_app_(name_app)
client = OpenAIKeysinit._init_client_(key_openai)
    
class CloudMd:
    def __init__(self,       
                appfb,
                client,          
                Logger: Optional[bool] = True,
                DebugTokens: Optional[bool] = True,
                lang: Optional[str] = "pt"
            ):
        self.appfb = appfb
        self.client = client
        self.Logger = Logger
        self.DebugTokens = DebugTokens
        self.lang = lang
        self.countNumberTokensTotal = 0
        self.key = "CloudMd"
        self.nameassistant = "Cloud Md"
        self.model_select = "gpt-4o-mini-2024-07-18"

        self.instruction = '''
        ## Objetivo
        Criar documentação técnica completa e de alta qualidade em formato **Markdown (.md)**, descrevendo de forma clara e objetiva os aspectos do software. O conteúdo deve ser acessível a membros da equipe de **suporte técnico**, facilitando a resolução de dúvidas e o entendimento das funcionalidades do sistema.

        ## Estrutura Recomendada

        ```markdown
        # Nome do Software

        ### Descrição
        A seção de Descrição deve fornecer uma visão abrangente e detalhada do software, estabelecendo uma base sólida para o entendimento do sistema como um todo. Comece apresentando o propósito fundamental do software, explicando claramente qual problema ele resolve e como se diferencia de outras soluções disponíveis no mercado. Detalhe os principais benefícios e vantagens competitivas, focando em como eles agregam valor para os usuários finais. Identifique e caracterize o público-alvo, incluindo suas necessidades específicas e como o software as atende. Liste todos os requisitos do sistema de forma detalhada, incluindo requisitos de hardware, software, rede e quaisquer outras dependências técnicas relevantes. Mantenha um registro claro da versão atual do software, incluindo as principais mudanças e melhorias implementadas em relação às versões anteriores. Esta seção deve servir como ponto de partida para qualquer pessoa que precise entender rapidamente o que é o software e como ele pode ser útil.

        ### Funcionalidades
        A documentação das funcionalidades deve ser extremamente detalhada e organizada de forma lógica, permitindo que os usuários encontrem rapidamente as informações necessárias. Comece com uma lista completa e categorizada de todas as funcionalidades disponíveis, agrupando-as por área ou tipo de uso. Para cada funcionalidade, forneça uma descrição detalhada que inclua: seu propósito específico, como acessá-la, os passos necessários para sua utilização, os resultados esperados e possíveis variações de uso. Inclua exemplos práticos e casos de uso comuns, demonstrando situações reais onde cada funcionalidade é mais útil. Documente claramente todas as limitações ou restrições existentes, como número máximo de registros, tipos de arquivos suportados ou requisitos específicos de permissão. Mapeie e explique as dependências entre diferentes funcionalidades, incluindo pré-requisitos e impactos em outras partes do sistema. Quando relevante, inclua dicas de otimização e melhores práticas para o uso eficiente de cada recurso.

        ### Navegação no Sistema
        A seção de navegação deve ser um guia completo e intuitivo que permita aos usuários compreenderem como se movimentar eficientemente pelo software. Comece com uma explicação detalhada da estrutura de menus, incluindo a hierarquia completa e a lógica de organização. Forneça descrições abrangentes de todas as telas principais, detalhando cada elemento da interface, incluindo campos, botões, ícones e suas respectivas funções. Documente todos os atalhos de teclado e recursos especiais de navegação que podem aumentar a produtividade. Descreva os fluxos de trabalho mais comuns de forma sequencial, incluindo capturas de tela ou diagramas quando necessário. Inclua dicas de usabilidade que ajudem os usuários a trabalhar de forma mais eficiente, como técnicas de filtro, ordenação e pesquisa. Explique como personalizar a interface (quando aplicável) e como acessar diferentes visualizações dos dados. Aborde também aspectos de acessibilidade e suporte a diferentes dispositivos ou resoluções de tela.

        ### Solução de Problemas
        Esta seção deve ser um recurso abrangente para resolução de problemas, organizado de forma a permitir uma rápida identificação e solução de questões comuns. Desenvolva um FAQ detalhado que cubra as dúvidas mais frequentes, organizadas por categoria e nível de complexidade. Crie um guia completo de troubleshooting que inclua uma metodologia sistemática para identificação e resolução de problemas, com árvores de decisão para diferentes cenários. Catalogue todas as mensagens de erro comuns, incluindo: o texto exato da mensagem, sua causa raiz, impacto no sistema, e passos detalhados para resolução. Documente procedimentos de recuperação para diferentes tipos de falhas, incluindo backup e restore, recuperação de dados e procedimentos de emergência. Mantenha um registro atualizado de cenários de falha conhecidos, incluindo workarounds e soluções temporárias quando aplicável. Inclua informações sobre ferramentas de diagnóstico disponíveis e como utilizá-las efetivamente.

        ### Atualizações e Manutenção
        A seção de atualizações e manutenção deve fornecer informações detalhadas sobre todos os aspectos de gestão do ciclo de vida do software. Mantenha um histórico de versões completo e bem documentado, incluindo: número da versão, data de lançamento, principais alterações, correções de bugs e novos recursos adicionados. Detalhe todos os procedimentos de backup necessários, incluindo frequência recomendada, dados que devem ser incluídos, método de execução e procedimentos de verificação. Documente as rotinas de manutenção preventiva, incluindo limpeza de dados, otimização de performance e verificações de integridade. Estabeleça um cronograma claro de atualizações, incluindo janelas de manutenção programadas e procedimentos de notificação aos usuários. Descreva detalhadamente os possíveis impactos das atualizações, incluindo tempo de indisponibilidade esperado, mudanças na interface ou funcionalidades e requisitos de treinamento. Inclua procedimentos de rollback para casos de problemas durante atualizações.

        ```

        ## Diretrizes de Escrita

        ### 1. Títulos e Subtítulos
        - Utilize # para o título principal e subtítulos
        - Mantenha uma hierarquia clara e consistente
        - Limite a profundidade a no máximo 3 níveis

        ### 2. Clareza e Objetividade
        - Use linguagem simples, clara e objetiva
        - Explique termos técnicos de forma acessível ou evite termos muito complexos
        - Evite o uso de exemplos de código ou detalhes técnicos irrelevantes para o suporte

        ### 3. Ênfase
        - Negrito para informações importantes
        - Itálico para termos técnicos ou conceitos-chave
        - Evite destacar elementos desnecessários

        ### 4. Organização
        - Estruture o conteúdo de forma lógica e sequencial
        - Divida o texto em seções curtas e objetivas
        - Utilize listas para facilitar a leitura de instruções ou funcionalidades

        ### 5. Foco na Experiência do Usuário
        - Descreva funcionalidades e fluxos de forma prática e funcional
        - Forneça instruções claras para instalação, configuração e resolução de problemas
        - Garanta que o documento possa ser utilizado como um guia rápido para dúvidas frequentes

        '''
        
        self.tools = [
        {
            "type": "function",
            "function": {
                "name": "autosave",
                "description": "Salva um codigo python em um caminho",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "codigo"
                        },
                        "path": {
                            "type": "string",
                            "description": "Caminho do codigo"
                        }
                    },
                    "required": ["code","path"]
                }
            }
        }
        ]
        
    def CloudMdCreateContent(self, filepath, nameforenv):
        """
        Gera documentação técnica em formato Markdown a partir de código Python,
        utilizando um agente de IA autenticado.
        """
        try:
            if self.Logger:
                if self.lang == "eng":
                    cprint(f'🔐 Authenticating AI agent for documentation generation...', 'blue', attrs=['bold'])
                else:
                    cprint(f'🔐 Autenticando agente de IA para geração de documentação...', 'blue', attrs=['bold'])

            AI, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(
                self.appfb, self.client, self.key, self.instruction, self.nameassistant, self.model_select, self.tools
            )

            if self.Logger:
                if self.lang == "eng":
                    cprint(f'✅ AI agent authenticated: {nameassistant} using model {model_select}', 'green')
                else:
                    cprint(f'✅ Agente de IA autenticado: {nameassistant} usando o modelo {model_select}', 'green')

            if self.Logger:
                if self.lang == "eng":
                    cprint('📤 Uploading files to the vector store...', 'yellow', attrs=['bold'])
                elif self.lang == "pt":
                    cprint('📤 Enviando arquivos para o repositório de vetores...', 'yellow', attrs=['bold'])

            AI = Agent_files_update.del_all_and_upload_files_in_vectorstore(self.appfb, self.client, AI, "CloudMd_Work_Environment", [filepath])

            if self.Logger:
                if self.lang == "eng":
                    cprint(f'✅ Files uploaded to vector store. AI updated: {AI}', 'yellow', attrs=['bold'])
                elif self.lang == "pt":
                    cprint(f'✅ Arquivos enviados para o repositório de vetores. AI atualizado: {AI}', 'yellow', attrs=['bold'])

            # if self.lang == "eng":
            #     mensagem_final = f"""
            #     Create comprehensive and high-quality technical documentation from Python source code stored in CloudMd_Work_Environment
            #     Save the final file in `.md` format (using autosave) in the following path:
            #     **D:\\Company Apps\\Projetos de codigo aberto\\SoftwareAI\\softwareai\\CoreApp\\Agents\\Software_Documentation\\{nameforenv}\\Docs\\{nameforenv}_(NameBasedInSourceCode.md)**
            #     in (NameBasedInSourceCode.md) create a name based on the source code and its function
            #     """
            # else:
            mensagem_final = f"""
            Crie a documentação técnica abrangente e de alta qualidade a partir do código-fonte Python armazenado em CloudMd_Work_Environment
            Salve o arquivo final no formato `.md` (usando autosave) no seguinte caminho:
            **D:\\Company Apps\\Projetos de codigo aberto\\SoftwareAI\\softwareai\\CoreApp\\Agents\\Software_Documentation\\{nameforenv}\\Docs\\{nameforenv}_{random.randint(2, 99)}.md**
            em (NameBasedInSourceCode.md) crie um nome baseado no codigo fonte e sua funcao
            """

            if self.Logger:
                if self.lang == "eng":
                    cprint(f'📝 Prepared prompt for documentation:\n{mensagem_final}', 'yellow')
                else:
                    cprint(f'📝 Prompt preparado para documentação:\n{mensagem_final}', 'yellow')

            adxitional_instructions = ""

            if self.Logger:
                if self.lang == "eng":
                    cprint(f'📤 Sending request to AI for documentation generation...', 'cyan')
                else:
                    cprint(f'📤 Enviando solicitação para IA gerar a documentação...', 'cyan')

            # Envio da mensagem para o agente de IA
            response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                mensagem=mensagem_final,
                agent_id=AI,
                key=self.key,
                app1=self.appfb,
                client=self.client,
                tools=self.tools,
                model_select=model_select,
                aditional_instructions=adxitional_instructions
            )

            if self.Logger:
                if self.lang == "eng":
                    cprint(f'📥 AI response received. Total tokens used: {total_tokens}', 'green')
                    cprint(f'🗒️ Documentation generated and saved for environment: {nameforenv}', 'green')
                else:
                    cprint(f'📥 Resposta da IA recebida. Total de tokens usados: {total_tokens}', 'green')
                    cprint(f'🗒️ Documentação gerada e salva para o ambiente: {nameforenv}', 'green')

            if self.DebugTokens:
                self.countNumberTokensTotal += total_tokens
                valor_min, valor_max = ResponseAgent.calculate_dollar_value(self.countNumberTokensTotal)
                if self.lang == "eng":
                    cprint(f'📜 Total Tokens Consumed: {self.countNumberTokensTotal} 💸${valor_min:.4f} and 💸${valor_max:.4f}', 'yellow', attrs=['bold'])
                elif self.lang == "pt":
                    cprint(f'📜 Total de Tokens Consumidos: {self.countNumberTokensTotal} 💸${valor_min:.4f} e 💸${valor_max:.4f}', 'yellow', attrs=['bold'])
                
        except Exception as e:
            if self.Logger:
                if self.lang == "eng":
                    cprint(f'❌ Error during documentation generation: {e}', 'red', attrs=['bold'])
                else:
                    cprint(f'❌ Erro durante a geração da documentação: {e}', 'red', attrs=['bold'])
            raise

    def Execute(self, softwarepath, nameforenv):
        """
        Executa o processo de cópia de arquivos .py e .MD de um diretório de software para diretórios específicos,
        e gera documentos Markdown a partir do conteúdo dos arquivos copiados.
        """
        try:
            # Caminho de destino para os códigos
            destpath = os.path.join(os.path.dirname(__file__), f"{nameforenv}", f"Codes")
            os.makedirs(destpath, exist_ok=True)
            
            if self.Logger:
                if self.lang == "eng":
                    cprint(f'📁 Created or confirmed existence of directory: {destpath}', 'green', attrs=['bold'])
                else:
                    cprint(f'📁 Diretório criado ou já existente: {destpath}', 'green', attrs=['bold'])
            
            # Caminho de destino para documentos
            nome_do_md = os.path.join(os.path.dirname(__file__), f"{nameforenv}", f"Docs") 
            os.makedirs(nome_do_md, exist_ok=True)
            
            if self.Logger:
                if self.lang == "eng":
                    cprint(f'📁 Created or confirmed existence of directory: {nome_do_md}', 'green', attrs=['bold'])
                else:
                    cprint(f'📁 Diretório criado ou já existente: {nome_do_md}', 'green', attrs=['bold'])

            # Listar arquivos .py e .MD no caminho do software
            listpy = [f for f in os.listdir(softwarepath) if f.startswith(('main'))]

            
            if self.Logger:
                if self.lang == "eng":
                    cprint(f'📄 Files to copy: {listpy}', 'cyan')
                else:
                    cprint(f'📄 Arquivos para copiar: {listpy}', 'cyan')

            # Copiar arquivos para o diretório de códigos
            for file in listpy:
                src_file = os.path.join(softwarepath, file)
                dest_file = os.path.join(destpath, file)
                shutil.copy(src_file, dest_file)
                
                if self.Logger:
                    if self.lang == "eng":
                        cprint(f'✅ Copied {file} to {dest_file}', 'green')
                    else:
                        cprint(f'✅ Arquivo {file} copiado para {dest_file}', 'green')

            # Listar novamente os arquivos copiados
            listpy = [f for f in os.listdir(softwarepath) if f.startswith(('main'))]
            
            # Processar cada arquivo copiado
            for py in listpy:
                nome_do_arquivo = os.path.join(destpath, py)
                nome_do_md = os.path.join(os.path.dirname(__file__), f"{nameforenv}", f"Docs", 
                                        f"{os.path.basename(nome_do_arquivo).replace('.md', '').replace('.MD', '').replace('.txt', '').replace('.py', '')}.md")

                if self.Logger:
                    if self.lang == "eng":
                        cprint(f'📖 Processing file: {nome_do_arquivo}', 'blue')
                    else:
                        cprint(f'📖 Processando arquivo: {nome_do_arquivo}', 'blue')

                with open(nome_do_arquivo, 'r+', encoding='utf-8') as file:
                    content = file.read()

                if self.Logger:
                    if self.lang == "eng":
                        cprint(f'🛠️ Generating Markdown from: {py}', 'yellow')
                    else:
                        cprint(f'🛠️ Gerando Markdown de: {py}', 'yellow')

                # Chamada para a função de geração de Markdown
                self.CloudMdCreateContent(nome_do_arquivo, nameforenv)

                if self.Logger:
                    if self.lang == "eng":
                        cprint(f'📄 Markdown generated for {py}', 'green')
                    else:
                        cprint(f'📄 Markdown gerado para {py}', 'green')
                        

                try:            
                    shutil.rmtree(os.path.join(os.path.dirname(__file__), f"{nameforenv}", f"Codes"))


                except Exception as e:
                    if self.Logger:
                        if self.lang == "eng":
                            cprint(f'❌ Error during execution: {e}', 'red', attrs=['bold'])
                        else:
                            cprint(f'❌ Erro durante a execução: {e}', 'red', attrs=['bold'])

                            
        except Exception as e:
            if self.Logger:
                if self.lang == "eng":
                    cprint(f'❌ Error during execution: {e}', 'red', attrs=['bold'])
                else:
                    cprint(f'❌ Erro durante a execução: {e}', 'red', attrs=['bold'])
            raise
