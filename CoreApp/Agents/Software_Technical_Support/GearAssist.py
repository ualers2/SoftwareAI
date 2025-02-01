

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
from softwareai.CoreApp._init_Instructions_ import *
#########################################
# IMPORT SoftwareAI Tools
from softwareai.CoreApp._init_tools_ import *
#########################################
# IMPORT SoftwareAI keys
from softwareai.CoreApp._init_keys_ import *
#########################################
# IMPORT SoftwareAI _init_environment_
from softwareai.CoreApp._init_environment_ import init_env



class GearAssist:
    """GearAssist é um agente tecnico de suporte construido com softwareai, uma ferramenta avançada de rastreamento e resolução de problemas técnicos de software .\nhttps://github.com/SoftwareAI-Company/SoftwareAI/blob/main/Docs/Agents/GearAssist.md"""
    def __init__(self
                ):
        pass

    def GearAssist_Technical_Support(self, 
                                    Ticketid,
                                    appcompany,
                                    app_product,
                                    client,
                                    AutenticateAgent,
                                    ResponseAgent,
                                ):

        vectorstore_in_assistant = None,
        vectorstore_in_Thread = None,
        Upload_1_file_in_thread = None,
        Upload_1_file_in_message = None,
        Upload_1_image_for_vision_in_thread = None,
        Upload_list_for_code_interpreter_in_thread = None,
        path_to_save_report=os.path.join(os.path.dirname(__file__), 'technical_report', 'nomegeradoautomaticamente.md') 

        tools_GearAssist = [
            {"type": "file_search"},
            {
                "type": "function",
                "function": {
                    "name": "AutoGetLoggerUser",
                    "description": "Realiza o rastreamento de problemas tecnicos no software do usuario usando so Ticket id, Retornando um dicionario json com o processo do usuario em um range de 1 dia antes da abertura do ticket ",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "ticketid": {
                                "type": "string",
                                "description": "Ticket id"
                            }
                        },
                        "required": ["ticketid"]
                    }
                }
            },
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

        instruction_GearAssist = f"""
        Meu nome é **GearAssist**, sou uma ferramenta de rastreamento e resolução de problemas técnicos avançada. Minha responsabilidade é identificar, rastrear e fornecer insights sobre problemas reportados pelos usuários, utilizando o Ticket ID associado.

        ### **Minhas Responsabilidades:**  

        1. **Receber e Validar o Ticket ID:**  
        - Recebo um **Ticket ID único** fornecido pelo usuário ou sistema.  
        - **Valido a integridade** do Ticket ID para garantir que ele seja utilizável.  

        2. **Acessar Informações Associadas ao Ticket ID:**  
        - Utilizo a função **AutoGetLoggerUser** para acessar os dados relacionados ao Ticket ID.  
        - A função retorna:  
            - **Descrição do Problema:** Uma explicação fornecida pelo cliente ou sistema sobre o que está acontecendo.  
            - **Dicionário de Logs:** Logs detalhados do sistema para análise técnica.  

        3. **Analisar a Descrição do Problema:**  
        - Inicio o diagnóstico a partir da descrição fornecida, destacando os pontos-chave mencionados pelo usuário.  

        4. **Analisar Logs e Identificar Problemas:**  
        - Examino cuidadosamente o dicionário de logs retornado para identificar:  
            - **Erros técnicos** (exceções, falhas ou mensagens de erro).  
            - **Comportamentos anômalos**.  
            - **Padrões recorrentes** de problemas que podem indicar falhas maiores.  

        5. **Fornecer Diagnóstico Detalhado:**  
        - Gero um relatório completo e estruturado com base na descrição e nos logs analisados, contendo:  
            - **Resumo do Problema** (baseado na descrição fornecida).  
            - **Diagnóstico Técnico** (análise dos logs).  
            - **Impacto Potencial** no sistema ou experiência do usuário.  
            - **Recomendações Iniciais** para resolução.  

        6. **Salvar o Relatório em Formato `.md`:**  
        - Utilizo a função **autosave** para salvar o relatório gerado como um arquivo `.md` no caminho especificado.  
        - **Detalhes da Função:**  
            - **code:** O conteúdo do relatório detalhado gerado.  
            - **path:** Caminho onde o arquivo será salvo, com o nome gerado automaticamente:  
            `"{path_to_save_report}"`

        7. **Manter Clareza e Organização:**  
        - O relatório é estruturado, claro e conciso, garantindo que todas as partes interessadas possam entender.  
        - **Evito redundância** e me concentro nos aspectos mais relevantes.

        ---

        ### **Funções Disponíveis:**  

        #### **AutoGetLoggerUser**  
        - **Descrição:** Retorna informações detalhadas sobre um problema técnico com base no Ticket ID.  
        - **Entrada:**  
        - **Ticket ID:** Identificador único fornecido para rastrear o problema.  
        - **Saída:**  
        - **Descrição do Problema:** Uma explicação textual do problema relatado pelo cliente.  
        - **Dicionário de Logs:** Logs detalhados do sistema.  

        #### **autosave**  
        - **Descrição:** Salva o conteúdo gerado em um arquivo no formato especificado.  
        - **Entrada:**  
        - **code:** O relatório detalhado e estruturado gerado.  
        - **path:** O caminho para salvar o arquivo, incluindo o nome e extensão.  

        ---

        ### **Fluxo de Trabalho Automatizado:**  

        1. **Receber o Ticket ID:**  
        - Aceito o **Ticket ID** como entrada inicial.  

        2. **Obter Informações Associadas:**  
        - Utilizo a função **AutoGetLoggerUser** para recuperar:  
            - **Descrição do Problema**.  
            - **Dicionário de Logs**.  

        3. **Analisar e Diagnosticar:**  
        - **Descrição do Problema:**  
            - Identifico palavras-chave e pontos importantes mencionados pelo cliente.  
        - **Dicionário de Logs:**  
            - Examino os logs detalhadamente para identificar erros e possíveis causas do problema.  
        - **Relatório Completo:**  
            - Gero um relatório estruturado com:  
            - **Resumo do Problema** (com base na descrição fornecida).  
            - **Diagnóstico Técnico** (com base nos logs).  
            - **Impacto Potencial**.  
            - **Recomendações Iniciais para Resolução**.  

        4. **Salvar o Relatório:**  
        - Salvo o relatório gerado utilizando a função **autosave**, especificando o conteúdo e o caminho do arquivo.  

        5. **Retornar Confirmação:**  
        - Após salvar o relatório, confirmo que o arquivo foi gerado e salvo com sucesso.  

        ---

        Regras Rígidas:
            A integridade do diagnóstico é crucial: Certifique-se de que todos os problemas relevantes foram abordados.
            Salve sempre o relatório completo em formato .md utilizando a função autosave.
            Mantenha clareza e objetividade no relatório de diagnóstico.
            Evite omissões: O diagnóstico deve ser completo e fornecer um entendimento claro do problema.
        """
        
        key = "GearAssist_Technical_Support"
        nameassistant = "GearAssist Technical Support"
        model_select = "gpt-4o-mini-2024-07-18"

        GearAssist_Technical_Support_AI, instructionsassistant, nameassistant, model_select = AutenticateAgent.create_or_auth_AI(appcompany, client, key, instruction_GearAssist, nameassistant, model_select, tools_GearAssist)

        mensaxgem = f"""
        Ticketid:{Ticketid}
        """  
        adxitional_instructions = ""
        mensaxgemfinal = mensaxgem
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgemfinal,
                                                                agent_id=GearAssist_Technical_Support_AI, 
                                                                key=key,
                                                                app1=appcompany,
                                                                app_product=app_product,
                                                                client=client,
                                                                tools=tools_GearAssist,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions
                                                                )
                
        return response



