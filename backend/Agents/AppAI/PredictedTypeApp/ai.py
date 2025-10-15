# Back-End\Agents\GitContextLayer\ai.py
from agents import Agent, Runner, ModelSettings
import logging
import os
from pydantic import BaseModel
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GeneratePredictedTypeAppAgent_logger")

class Predictedtypeapp(BaseModel):
    type_app: str
    justificativa: str


async def GeneratePredictedTypeAppAgent(
        OPENAI_API_KEY,
        user_id,
        user_content,
        commit_language = 'pt',
        model = "gpt-5-nano",
    ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    logger.info(f"Predicted Type App Agent")

    total_usage = {
        "input": 0, "cached": 0, "reasoning": 0, "output": 0, "total": 0
    }
    logger.info(f"language {commit_language}")
    
    if commit_language == 'en':
        prompt_system_direct = f"""

        """

    elif commit_language == 'pt':
        prompt_system_direct = f"""
Você é um arquiteto de soluções especialista em classificação de ideias de software.

Sua tarefa é analisar a descrição fornecida pelo usuário sobre um sistema, site ou aplicativo que ele deseja criar e **determinar qual tipo de aplicação melhor representa o pedido**, escolhendo entre:

1. "site" → site institucional simples, página de apresentação, blog ou landing page.
2. "portfólio" → site pessoal ou de empresa voltado à exibição de trabalhos, currículos ou projetos.
3. "ecommerce" → loja virtual, marketplace ou sistema com carrinho de compras, pagamentos e produtos.
4. "projeto" → aplicação customizada, painel administrativo, dashboard interno ou solução de nicho sem fins comerciais diretos.
5. "saas" → sistema online baseado em assinatura, com múltiplos usuários e funcionalidades autônomas entregues pela nuvem.

---

### Instruções:

1. Leia atentamente o texto do usuário.
2. Analise o propósito principal, público-alvo e características funcionais.
3. Escolha o tipo mais apropriado com base no contexto.
4. Retorne **somente um objeto JSON válido**, conforme o esquema:

"tipo_app": "site | portfólio | ecommerce | projeto | saas",
"justificativa": "Explicação curta (1 a 2 frases) descrevendo o motivo da classificação."

        """


    agent = Agent(
        name="Agent Predicted Type App",
        instructions=prompt_system_direct,
        model=model,
        output_type=Predictedtypeapp,
        model_settings=ModelSettings(include_usage=True)
    )
    result = await Runner.run(agent, user_content, max_turns=300)
    type_app = result.final_output.type_app
    justificativa = result.final_output.justificativa

    usage = result.context_wrapper.usage
    total_usage["input"] = usage.input_tokens
    total_usage["cached"] = usage.input_tokens_details.cached_tokens
    total_usage["reasoning"] = usage.output_tokens_details.reasoning_tokens
    total_usage["output"] = usage.output_tokens
    total_usage["total"] = usage.total_tokens

    logger.info(f"Agent Final Usage: {total_usage['total']} total tokens.")
    return type_app, justificativa, total_usage["total"]







