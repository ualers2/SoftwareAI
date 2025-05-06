



# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

from softwareai_engine_library.Chat.history.save_history_user import save_history_user
from softwareai_engine_library.Chat.history.save_history_system import save_history_system
from softwareai_engine_library.Chat.stream.send_to_webhook import send_to_webhook
from softwareai_engine_library.Chat.tokens._o3_mini import *


async def process_stream(type_stream,
                        agent, 
                        attach_message, 
                        WEBHOOK_URL,
                        session_id,
                        user_email,
                        appcompany
                        ):
    # global input_tokens
    # global cached_tokens
    # global reasoning_tokens
    # global completion_tokens
    # global total_tokens


    input_tokens = 0
    cached_tokens = 0
    reasoning_tokens = 0
    completion_tokens = 0
    total_tokens = 0
    cost_instr = 0.0
    cost_out = 0.0

    save_history_user(
        session_id,
        user_email,
        attach_message,
        appcompany
            
        )

    result = Runner.run_streamed(
        agent,
        attach_message,
        max_turns=500
    )
    print("=== Run starting ===")

    try:
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                if type_stream == "real_stream":
                    send_to_webhook(
                        WEBHOOK_URL=WEBHOOK_URL,
                        user="Chat Agent",
                        type="real_stream",
                        message=event.data.delta
                    )
                else:
                    continue
            # When the agent updates, print that
            elif event.type == "agent_updated_stream_event":
                message_to_send = f"Agent: {event.new_agent.name}"
                if type_stream == "info":
                    send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                elif type_stream == "agentworkflow":  
                    send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                elif type_stream == "real_stream":
                    pass

                if type_stream == "real_stream":     
                    pass
                else:       
                    save_history_system(
                        session_id,
                        user_email,
                        message_to_send,
                        appcompany
                            
                    )
    
            # When items are generated, print them
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    message_to_send = f"{event.item.agent.name} -- Tool was called"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass


                    if type_stream == "real_stream":     
                        pass
                    else:       
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )

                elif event.item.type == "tool_call_output_item":
                    message_to_send = f"{event.item.agent.name} -- Tool output: {event.item.raw_item}"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass


                    if type_stream == "real_stream":     
                        pass
                    else:       
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )
                        output_data = event.item.raw_item.get("output", "")
                        
                        try:
                            # Substitui aspas simples por aspas duplas para garantir um formato JSON válido
                            if isinstance(output_data, str):
                                output_data = output_data.replace("'", "\"")
                                parsed_output = json.loads(output_data)  # Usando json.loads() em vez de eval
                            else:
                                parsed_output = output_data

                            print(f"parsed_output: {parsed_output}")
                            print(f"output_data: {output_data}")

                            file_path = parsed_output.get("file_path")
                            # send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"file_path: {file_path}")
                            # send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"parsed_output: {parsed_output}")
                            # send_to_webhook(WEBHOOK_URL, "Chat Agent", "info", f"output_data: {output_data}")

                            if file_path:
                                with open(file_path, "rb") as f:
                                    file_bytes = f.read()
                                    file_base64 = base64.b64encode(file_bytes).decode("utf-8")

                                # Envia o conteúdo do arquivo direto pro webhook
                                send_to_webhook(
                                    WEBHOOK_URL,
                                    user="Chat Agent",
                                    type="file",
                                    message={
                                        "file_name": file_path,
                                        "file_base64": file_base64
                                    }
                                )
                            else:
                                pass

                        except Exception as e:
                            print(f" Erro ao processar o output: {str(e)}")
                        
                        
                elif event.item.type == "reasoning_item":
                    message_to_send = f"{event.item.agent.name} -- Reasoning"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass

                    if type_stream == "real_stream":     
                        pass
                    else:      
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )
                elif event.item.type == 'handoff_call_item':
                    message_to_send = f"{event.item.agent.name} -- handoff was called"
                    if type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info", message=message_to_send)
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "real_stream":
                        pass

                    if type_stream == "real_stream":     
                        pass
                    else:      
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                            )
                    
                elif event.item.type == "message_output_item":
                    message_to_send = f"{event.item.agent.name} -- {ItemHelpers.text_message_output(event.item)}"
                    
                    if type_stream == "real_stream":
                        pass
                    elif type_stream == "agentworkflow":  
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="agentworkflow", message=message_to_send)
                    elif type_stream == "info":
                        send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="info",  message=message_to_send)

                    if type_stream == "real_stream":     
                        pass
                    else:     
                        save_history_system(
                            session_id,
                            user_email,
                            message_to_send,
                            appcompany
                                
                            )
                    

                else:
                    pass  # Ignore other event types

            # Capturar o evento final já embrulhado em RawResponsesStreamEvent:
            elif event.type == "raw_response_event" and isinstance(event.data, ResponseCompletedEvent):
                usage = event.data.response.usage
                input_tokens      += usage.input_tokens
                cached_tokens     += usage.input_tokens_details.cached_tokens
                reasoning_tokens  += usage.output_tokens_details.reasoning_tokens
                completion_tokens += usage.output_tokens
                total_tokens      += usage.total_tokens
                cost_instr += round(input_tokens * cost_instruction_token , 6)
                cost_out += round(total_tokens * cost_output_token, 6) 
                cost_total = round(cost_instr + cost_out, 6)
                
                # print(f"input_tokens: {input_tokens}")
                # print(f"cached_tokens: {cached_tokens}")
                # print(f"reasoning_tokens: {reasoning_tokens}")
                # print(f"completion_tokens: {completion_tokens}")
                # print(f"total_tokens: {total_tokens}")

                # send_to_webhook(WEBHOOK_URL=WEBHOOK_URL, user="Chat Agent", type="usage_summary", message={
                #     "input_tokens": usage.input_tokens,
                #     "cached_tokens": usage.input_tokens_details.cached_tokens,
                #     "reasoning_tokens": usage.output_tokens_details.reasoning_tokens,
                #     "completion_tokens": usage.output_tokens,
                #     "total_tokens": usage.total_tokens
                # })


    except Exception as e:
        # trate erros aqui, se necessário
        pass
    else:

        if type_stream == "real_stream":     
            pass
        else:   
            # 4) ao sair do loop SEM erro, envia o resumo agregado
            send_to_webhook(
                WEBHOOK_URL=WEBHOOK_URL,
                user="Chat Agent",
                type="usage_summary",
                message={
                    "cost_total": cost_total,
                    "cost_out":      cost_out,
                    "cost_instr":      cost_instr,
                    "input_tokens":      input_tokens,
                    "cached_tokens":     cached_tokens,
                    "reasoning_tokens":  reasoning_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens":      total_tokens,
                }
            )

            send_to_webhook(
                WEBHOOK_URL=WEBHOOK_URL,
                user="Chat Agent",
                type="stream_end",
                message={
                    "cost_total": cost_total,
                }
            )
    print("=== Run complete ===")
