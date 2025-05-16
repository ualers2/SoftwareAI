


from softwareai_engine_library.Chat.stream.process_stream import process_stream


async def process_stream_and_save_history(
                            type_stream,
                            agent_,
                            message,
                            WEBHOOK_URL,
                            session_id,
                            user_email,
                            number,
                            appcompany
                            
                            
                            ):
    await process_stream(type_stream, 
                        agent_, 
                        message, 
                        WEBHOOK_URL,
                        session_id,
                        user_email,
                        appcompany
                                        
                    )
    print(f"🤖Sistema {number}")

    