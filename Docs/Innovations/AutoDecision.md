# bem para que agentes softwareai se juntarem de fato a força de trabalho precisamos de uma tomada de decisao mais precisa 
oque usavamos no inicio 
```python

        mensaxgem = """decida oque o usuario esta solicitando com base na mensagem  
        Regra 1 - Caso seja solicitado algum script ou software Responda no formato JSON Exemplo: {'solicitadoalgumcodigo': 'solicitacao...'} 
        Regra 2 - Caso seja solicitado alguma atualização de repositorio Responda no formato JSON Exemplo: {'solicitadoatualizaçãoderepositorio': 'somente o nome do repositorio que o usuario informou'}
        Regra 3 - Caso seja solicitado alguma criação de repositorio use a function (create_repo) 
        """  


            
        mensaxgemfinal = mensaxgem + f"mensagem:\n{mensagem}"
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgemfinal,
                                                                agent_id=AI_ByteManager, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_ByteManager,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_ByteManager
                                                                )
                                                
                
    if 'solicitadoatualizaçãoderepositorio' in teste_dict:

        repo_name = teste_dict['solicitadoatualizaçãoderepositorio'] 

        init_env(repo_name)

        Melhorias = self.SoftwareDevelopment.QuantumCoreUpdate(
            appfb, client, repo_name
            )
```
```python

        mensaxgem = """decida oque o usuario esta solicitando com base na mensagem e aplique as regras para cada caso
        Regra 1 - Caso seja solicitado algum script ou software Responda no formato JSON Exemplo: {'solicitadoalgumcodigo': 'solicitacao...'} 
        Regra 2 - Caso seja solicitado alguma atualização de repositorio use a function (autoupdaterepo)
        Regra 3 - Caso seja solicitado alguma criação de repositorio use a function (create_repo) 
        """  
            
        mensaxgemfinal = mensaxgem + f"mensagem:\n{mensagem}"
        
        response, total_tokens, prompt_tokens, completion_tokens = ResponseAgent.ResponseAgent_message_with_assistants(
                                                                mensagem=mensaxgemfinal,
                                                                agent_id=AI_ByteManager, 
                                                                key=key,
                                                                app1=appfb,
                                                                client=client,
                                                                tools=tools_ByteManager,
                                                                model_select=model_select,
                                                                aditional_instructions=adxitional_instructions_ByteManager
                                                                )
                                                
              
```
# autoupdaterepo
```python

def autoupdaterepo(repo_name, appfb, client, SoftwareDevelopment):

    init_env(repo_name)

    Melhorias = SoftwareDevelopment.QuantumCoreUpdate(
        appfb, client, repo_name
        )
           
```
