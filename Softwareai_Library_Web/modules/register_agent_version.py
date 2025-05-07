import time
from firebase_admin import db

def register_agent_version(
                            icon,
                            type_plan,
                            agent_id,
                            shortDescription,
                            fullDescription,
                            UseCases,
                            instruction,
                            instruction_path,
                            tutorial,
                            model_agent,
                            name_agent,
                            tools_agent,
                            new_hash, 
                            firebase_app,
                            logger
                                    
                    
                           ) -> None:
    """
    Registra no RTDB um novo snapshot cumulativo do metadata do agente.
    """
    
    base_ref_agent = db.reference(f"agents/{agent_id}/metadata", app=firebase_app)

    base_ref_history = db.reference(f"agents/{agent_id}/history/versions", app=firebase_app)
    existing = base_ref_history.get() or {}

    # evita duplicatas
    for ver, data in existing.items():
        if data.get('hash') == new_hash:
            logger.info(f"[skip] Hash já existe para {agent_id}")
            return

    version_num = len(existing) + 1
    ver_key = f"v{version_num}"
    timestamp = time.time()

    base_ref_history.child(ver_key).set({
        'icon': icon,
        'shortDescription': shortDescription,
        'fullDescription': fullDescription,
        'UseCases': UseCases,
        'instruction': instruction,
        'tutorial': tutorial,
        'model': model_agent,
        'name': name_agent,
        'tools': tools_agent,
        'version': ver_key,
        'hash': new_hash,
        'timestamp': timestamp
    })

    base_ref_agent.set({
        'icon': icon,
        'type_plan': type_plan,
        'shortDescription': shortDescription,
        'fullDescription': fullDescription,
        'UseCases': UseCases,
        'instruction': instruction,
        'tutorial': tutorial,
        'model': model_agent,
        'name': name_agent,
        'tools': tools_agent,
    })

    # atualiza latest
    db.reference(f"agents/{agent_id}/history/latest", app=firebase_app).set(ver_key)
    logger.info(f"[new] Versão {ver_key} registrada para {agent_id}")
