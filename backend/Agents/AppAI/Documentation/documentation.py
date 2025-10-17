# Employees\Documentation\server\documentation.py
from agents import Agent,  ItemHelpers, Runner,RunHooks, handoff, ModelSettings , RunConfig, RunContextWrapper, Usage
import asyncio
import logging
import os
from firebase_admin import db
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from openai.types.responses import ResponseCompletedEvent, ResponseTextDeltaEvent
import requests
from dotenv import load_dotenv
import math
from typing import List, Dict, Any, Tuple


#########################################
from Modules.Helpers.EgetTools import *
#########################################

diretorio_script = os.path.dirname(__file__) 
os.makedirs(os.path.join(diretorio_script, 'Logs'), exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(os.path.join(diretorio_script, 'Logs', 'documentation.log'))
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "Keys", "env.env"))

PRODUCTION_ENV = os.getenv("PRODUCTION_ENV", "True")
path_keys_ = os.path.join(diretorio_script, 'Keys', 'keys.env')
load_dotenv(dotenv_path=path_keys_)
if PRODUCTION_ENV == "True":
    pass
elif PRODUCTION_ENV == "False":
    pass

MAX_INPUT_SIZE = 40000

class Path_Att(BaseModel):
    Trust: str
    DocumentationType: str
    FilesAnalyzed: str
    ChangeSummary: str
    DocumentationScope: str
    GeneratedDocs: str
    UpdatedSections: str
    PRbody: str

class SummaryOutput(BaseModel):
    Trust: str
    DocumentationType: str
    FilesAnalyzed: str
    ChangeSummary: str
    DocumentationScope: str
    GeneratedDocs: str
    UpdatedSections: str
    PRbody: str

class Data(BaseModel):
    message_input: str


async def on_handoff(ctx: RunContextWrapper[None], input_data: Data):
    print(f"ConstructJunior: {input_data.message_input}")


async def ConstructJunior(
        python_paths,
        name="Employer 4: AI Junior Documentation",
        model="gpt-5-nano",
        Instructions_file="",
    ):
    python_paths_str = str(python_paths)
    file_prompt_path = os.path.join(diretorio_script, "Instructions", Instructions_file)
    with open(file_prompt_path, "r", encoding="utf-8") as file_prompt:
        prompt_system_ = file_prompt.read()
        prompt_system = f"""{prompt_system_} \n

```
autosave:
  path: "{python_paths_str}"
  code: "<conteúdo completo da documentação>"

```
"""  

    Tools_Softwareai_dict = Egetoolsv2(["autosave"])

    agent = Agent(
            name=name, 
            instructions=prompt_system,
            model=model, 
            output_type=Path_Att,
            # tools=Tools_Softwareai_dict
        )

    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=Data,
    )
    return agent, handoff_obj


async def ConstructSummaryAgent(
        python_paths,
        name="Documentation Summary Agent",
        model="gpt-5-nano"
    ):
    """Cria o agente de sumarização final"""
    python_paths_str = str(python_paths).replace("[", "").replace("[", "]")
    summary_prompt = f"""Você é um agente especializado em sumarizar e consolidar múltiplas respostas de documentação em uma única resposta coerente e completa.

## INSTRUÇÕES:
1. Receba múltiplas respostas de documentação de chunks processados
2. Consolide as informações removendo redundâncias
3. Mantenha a estrutura JSON original
4. Garanta coerência e fluxo narrativo
5. Combine seções relacionadas de forma inteligente


## FORMATO DE SAÍDA:
Retorne apenas um JSON válido consolidando todas as informações dos chunks:

- Trust: consolide os percentuais (use o mais conservador se houver conflito)
- DocumentationType: unifique tipos similares ou use o mais abrangente
- FilesAnalyzed: combine listas removendo duplicatas
- ChangeSummary: crie um resumo coerente das mudanças de todos os chunks
- DocumentationScope: unifique o escopo total da documentação
- GeneratedDocs: combine toda a documentação em um fluxo lógico
- UpdatedSections: liste todas as seções únicas atualizadas
- PRbody: crie um PR body unificado e coerente

Ao final, salve os arquivos de documentação usando a ferramenta `autosave`:


```
autosave:
  path: "{python_paths_str}"
  code: "<conteúdo completo da documentação>"

```

**Assegure-se de que o campo `code` contenha a documentação completa, bem formatada.**

IMPORTANTE: Mantenha a qualidade técnica e evite repetições desnecessárias."""

    Tools_Softwareai_dict = Egetoolsv2(["autosave"])

    agent = Agent(
        name=name, 
        instructions=summary_prompt,
        model=model, 
        output_type=SummaryOutput,
        tools=Tools_Softwareai_dict
    )
    
    return agent


async def Junior(
        python_paths,
        content_request,
        model="gpt-5-nano",
        Instructions_file="documentação.md",
    ):

    agent, handoff_obj = await ConstructJunior(
        python_paths,
        model=model,
        Instructions_file=Instructions_file,
    )
    
    input_size = len(content_request.encode("utf-8"))
    logger.info(f"Tamanho em bytes: {input_size}")

    if input_size > MAX_INPUT_SIZE:
        logger.info(f"Conteúdo ({input_size} bytes) acima do limite ({MAX_INPUT_SIZE} bytes). Processando com contexto acumulado.")
        
        # Dividir em chunks
        linhas = content_request.splitlines(keepends=True)
        chunk_size = math.ceil(len(linhas) / math.ceil(input_size / MAX_INPUT_SIZE))
        chunks = []
        
        for i in range(0, len(linhas), chunk_size):
            chunk = "".join(linhas[i:i + chunk_size])
            chunks.append(chunk)
        
        logger.info(f"Dividido em {len(chunks)} chunks.")
        
        # Processar chunks com contexto acumulado
        accumulated_context = ""
        chunk_responses = []
        
        for i, chunk in enumerate(chunks):
            logger.info(f"Processando chunk {i+1}/{len(chunks)}")
            
            # Primeiro chunk: processa normalmente
            if i == 0:
                input_with_context = f"""
CHUNK {i+1}/{len(chunks)}:

{chunk}

INSTRUÇÕES ESPECIAIS:
- Este é o chunk {i+1} de {len(chunks)} chunks
- Processe este conteúdo e gere documentação parcial
- Mantenha foco nas mudanças identificadas neste chunk
- Esta documentação será consolidada com outros chunks posteriormente
"""
            else:
                # Chunks subsequentes: inclui contexto dos chunks anteriores
                input_with_context = f"""
CONTEXTO DOS CHUNKS ANTERIORES:
{accumulated_context}

---

CHUNK ATUAL {i+1}/{len(chunks)}:

{chunk}

INSTRUÇÕES ESPECIAIS:
- Este é o chunk {i+1} de {len(chunks)} chunks
- Use o contexto dos chunks anteriores para manter coerência
- Processe este chunk complementando a documentação já iniciada
- Evite repetir informações já documentadas nos chunks anteriores
- Esta documentação será consolidada com outros chunks posteriormente
"""

            result = await Runner.run(agent, input_with_context, max_turns=300)
            final_output = result.final_output
            
            chunk_responses.append(final_output)
            
            # Atualizar contexto acumulado (resumo das respostas anteriores)
            if final_output:
                context_summary = f"""
Chunk {i+1} processado:
- Tipo de Documentação: {final_output.DocumentationType}
- Arquivos Analisados: {final_output.FilesAnalyzed}
- Resumo das Mudanças: {final_output.ChangeSummary}
- Escopo da Documentação: {final_output.DocumentationScope}
"""
                accumulated_context += context_summary
                
            logger.info(f"Chunk {i+1} processado. Contexto acumulado atualizado.")
        
        # Usar agente de sumarização para consolidar todas as respostas
        logger.info("Iniciando consolidação das respostas dos chunks...")
        summary_agent = await ConstructSummaryAgent(python_paths, model=model)
        
        # Preparar input para o agente de sumarização
        consolidation_input = "RESPOSTAS DOS CHUNKS PARA CONSOLIDAÇÃO:\n\n"
        for i, response in enumerate(chunk_responses):
            consolidation_input += f"""
CHUNK {i+1} RESPONSE:
Trust: {response.Trust}
DocumentationType: {response.DocumentationType}
FilesAnalyzed: {response.FilesAnalyzed}
ChangeSummary: {response.ChangeSummary}
DocumentationScope: {response.DocumentationScope}
GeneratedDocs: {response.GeneratedDocs}
UpdatedSections: {response.UpdatedSections}
PRbody: {response.PRbody}

---

"""
        
        consolidation_input += "\nCONSOLIDE TODAS AS RESPOSTAS ACIMA EM UMA ÚNICA RESPOSTA COERENTE E COMPLETA."
        
        final_result = await Runner.run(summary_agent, consolidation_input, max_turns=300)
        final_consolidated = final_result.final_output
        
        logger.info("Consolidação concluída.")
        
        return (
            final_consolidated.Trust.strip(), 
            final_consolidated.DocumentationType.strip(),
            final_consolidated.FilesAnalyzed, 
            final_consolidated.ChangeSummary.strip(), 
            final_consolidated.DocumentationScope.strip(), 
            final_consolidated.GeneratedDocs.strip(),
            final_consolidated.UpdatedSections.strip(),
            final_consolidated.PRbody.strip(),
        )

    # Input pequeno: processa normalmente
    result = await Runner.run(agent, content_request, max_turns=300)
    final_output = result.final_output
    logger.info(f"RAW OUTPUT: {final_output}")

    return (
        final_output.Trust.strip() if final_output.Trust else "", 
        final_output.DocumentationType.strip() if final_output.DocumentationType else "",
        final_output.FilesAnalyzed if final_output.FilesAnalyzed else [], 
        final_output.ChangeSummary.strip() if final_output.ChangeSummary else "", 
        final_output.DocumentationScope.strip() if final_output.DocumentationScope else "", 
        final_output.GeneratedDocs.strip() if final_output.GeneratedDocs else "",
        final_output.UpdatedSections.strip() if final_output.UpdatedSections else "",
        final_output.PRbody.strip() if final_output.PRbody else "",
    )


async def main(python_paths, content_request, model):
    """Versão melhorada usando processamento híbrido robusto para múltiplos arquivos"""

    (Trust, 
        DocumentationType,
        FilesAnalyzed, 
        ChangeSummary, 
        DocumentationScope, 
        GeneratedDocs,
        UpdatedSections,
        PRbody,
    ) = await Junior(
        python_paths=python_paths,
        content_request=content_request, 
        model=model
    )
    return (Trust, 
        DocumentationType,
        FilesAnalyzed, 
        ChangeSummary, 
        DocumentationScope, 
        GeneratedDocs,
        UpdatedSections,
        PRbody,
    )


if __name__ == "__main__":
    file_prompt_path = os.path.join(diretorio_script, "../", "Keys", "keys.env")
    load_dotenv(dotenv_path=file_prompt_path)
    workenv =  os.path.abspath(os.path.join(diretorio_script, '../', "Core", "WorkEnv", "Project1"))
    os.chdir(workenv)
    python_path_new = r"C:\Users\Media Cuts DeV\Downloads\HomeServer\HomeServer\Employees\FrontEnd\server\storage\files\2025\08\30\465e1030f12b4ae4a85ad483b3e1d655_server.py"
    python_path_old = r"C:\Users\Media Cuts DeV\Downloads\HomeServer\HomeServer\Employees\FrontEnd\server\storage\files\2025\08\30\server.py"

    with open(python_path_new, "r", encoding="utf-8") as file_python2:
        content_python_path_new = file_python2.read()
        file_python2.close()
    with open(python_path_old, "r", encoding="utf-8") as file_python:
        content_python_path_old = file_python.read()
        file_python.close()

    problem_ = f""" 
    old \n
    {content_python_path_old}\n
    new\n
    {content_python_path_new}
    """
    Trust, DocumentationType, FilesAnalyzed, ChangeSummary, DocumentationScope, GeneratedDocs, UpdatedSections, PRbody = asyncio.run(main(
        [workenv],
        problem_,
        model="gpt-5-nano"
    ))