# Back-End\Agents\GitContextLayer\ai.py
from agents import Agent, Runner, ModelSettings
import logging
import os
from pydantic import BaseModel
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GitContextLayer_logger")

class CommitMessageOutput(BaseModel):
    subject: str
    body: str

class CommitChunkSummary(BaseModel):
    summary_points: str

async def GenerateCommitMessageAgent(
        OPENAI_API_KEY,
        user_id,
        diff,
        files,
        commit_language = 'pt',
        model = "gpt-5-nano",
        MAX_INPUT_SIZE: int = 40000,
    ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    diff_size = len(diff.encode("utf-8"))
    logger.info(f"Commit Agent - Diff size (bytes): {diff_size}")

    total_usage = {
        "input": 0, "cached": 0, "reasoning": 0, "output": 0, "total": 0
    }
    logger.info(f"language {commit_language}")
    

    if diff_size > MAX_INPUT_SIZE:
        logger.info(f"Diff exceeds {MAX_INPUT_SIZE} bytes. Initiating chunking process.")
        

        if commit_language == 'en':
            prompt_chunk_analyzer = f"""
            You are part of a multi-step analysis pipeline. Your task is to analyze a CHUNK of a larger diff.
            Do NOT write a final commit message. Instead, extract and list the most significant changes from this chunk as concise bullet points.
            Focus only on the technical changes presented in the text provided.
            Your output MUST be a valid JSON object conforming to the `CommitChunkSummary` schema.
            """
            
            prompt_final_summarizer = f"""
            You are a Git expert responsible for synthesizing multiple analysis summaries into a final, high-quality commit message.
            You will receive a list of bullet points summarizing changes from different parts of a large diff.
            Your task is to consolidate these points, remove redundancy, and generate a single, cohesive commit message.

            Your output MUST be a valid JSON object conforming to the `CommitMessageOutput` schema, with:
            - 'subject': A concise, imperative line (max 72 chars).
            - 'body': A detailed explanation of the 'what' and 'why', based on the provided summaries.
            
            Respond in English
            """

        elif commit_language == 'pt':
            prompt_chunk_analyzer = f"""
            Você faz parte de um pipeline de análise de várias etapas. Sua tarefa é analisar um CHUNK de um diff maior.
            NÃO escreva uma mensagem de commit final. Em vez disso, extraia e liste as alterações mais significativas deste chunk como tópicos concisos.
            Concentre-se apenas nas alterações técnicas apresentadas no texto fornecido.
            Sua saída DEVE ser um objeto JSON válido em conformidade com o esquema `CommitChunkSummary`.
            """
            
            prompt_final_summarizer = f"""
            Você é um especialista em Git responsável por sintetizar múltiplos resumos de análise em uma mensagem de commit final e de alta qualidade.
            Você receberá uma lista de tópicos resumindo as alterações de diferentes partes de um diff grande.
            Sua tarefa é consolidar esses pontos, remover redundâncias e gerar uma mensagem de commit única e coesa.

            Sua saída DEVE ser um objeto JSON válido em conformidade com o esquema `CommitMessageOutput`, com:
            - 'subject': Uma linha concisa e imperativa (máximo de 72 caracteres).
            - 'body': Uma explicação detalhada de 'o quê' e 'por quê', com base nos resumos fornecidos.
            
            Responda em portugues
            """

        chunks = split_chunks(diff, MAX_INPUT_SIZE)
        logger.info(f"Diff split into {len(chunks)} chunks.")

        summaries = []
        for i, chunk in enumerate(chunks, 1):

            if commit_language == 'en':
                chunk_content = f"""
                Analyzing chunk {i}/{len(chunks)} of a large diff.
                Modified files for context: {", ".join(files[:10])}{"..." if len(files) > 10 else ""}
                
                Diff Chunk:
                ```diff
                {chunk}
                ```
                """
            elif commit_language == 'pt':
                chunk_content = f"""
                Analisando o bloco {i}/{len(chunk)} de uma grande diferença.
                Arquivos modificados para contexto: {", ".join(files[:10])}{"..." if len(files) > 10 else ""}

                Bloco de Diferença:
                ```diff
                {chunk}
                ```
                """
            agent_chunk = Agent(
                name=f"CommitChunkAnalyzer_{i}",
                instructions=prompt_chunk_analyzer,
                model=model,
                output_type=CommitChunkSummary,
                model_settings=ModelSettings(include_usage=True)
            )
            result = await Runner.run(agent_chunk, chunk_content, max_turns=1)
            summaries.append(result.final_output.summary_points)

            usage = result.context_wrapper.usage
            total_usage["input"] += usage.input_tokens
            total_usage["cached"] += usage.input_tokens_details.cached_tokens
            total_usage["reasoning"] += usage.output_tokens_details.reasoning_tokens
            total_usage["output"] += usage.output_tokens
            total_usage["total"] += usage.total_tokens


        if commit_language == 'en':
            combined_summary = f"""
            Context:
            - Modified files: {", ".join(files)}

            Aggregated summaries from all diff chunks:
            ---
            {chr(10).join(summaries)}
            ---
            Please synthesize this information into the final commit message.
            """
        
        elif commit_language == 'pt':
            combined_summary = f"""
            Contexto:
            - Arquivos modificados: {", ".join(files)}

            Resumos agregados de todos os blocos de diff:
            ---
            {chr(10).join(summaries)}
            ---
            Por favor, sintetize essas informações na mensagem de commit final.
            """
            
        agent_summarizer = Agent(
            name="CommitSummarizer",
            instructions=prompt_final_summarizer,
            model=model,
            output_type=CommitMessageOutput,
            model_settings=ModelSettings(include_usage=True)
        )
        result = await Runner.run(agent_summarizer, combined_summary, max_turns=1)
        commit_message = result.final_output.body
        commit_title = result.final_output.subject

        usage = result.context_wrapper.usage
        total_usage["input"] += usage.input_tokens
        total_usage["cached"] += usage.input_tokens_details.cached_tokens
        total_usage["reasoning"] += usage.output_tokens_details.reasoning_tokens
        total_usage["output"] += usage.output_tokens
        total_usage["total"] += usage.total_tokens

    else:
        
        logger.info("Diff size is within limits. Using direct processing.")
        
        if commit_language == 'en':
            prompt_system_direct = f"""
            You are a Git expert tasked with writing clear, informative commit messages.
            Analyze the provided code changes (diff) and the list of modified files.
            Your output MUST be a valid JSON object conforming to the `CommitMessageOutput` schema, with:
            - 'subject': A concise, imperative line (max 72 chars).
            - 'body': A detailed explanation of the 'what' and 'why' of the change.
            Respond in English
            """

            user_content = f"""
            Context for analysis:
            Modified files ({len(files)}):
            {chr(10).join(f"- {f}" for f in files)}
            
            Diff:
            ```diff
            {diff}
            ```
            """

        elif commit_language == 'pt':
            prompt_system_direct = f"""
            Você é um especialista em Git encarregado de escrever mensagens de commit claras e informativas.
            Analise as alterações de código fornecidas (diff) e a lista de arquivos modificados.
            Sua saída DEVE ser um objeto JSON válido em conformidade com o esquema `CommitMessageOutput`, com:
            - 'subject': Uma linha concisa e imperativa (máx. 72 caracteres).
            - 'body': Uma explicação detalhada do 'o quê' e do 'porquê' da alteração.
            Responda em portugues
            """

            user_content = f"""
            Contexto para análise:
            Arquivos modificados ({len(files)}):
            {chr(10).join(f"- {f}" for f in files)}
            
            Diff:
            ```diff
            {diff}
            ```
            """
        
        agent = Agent(
            name="CommitMessageGeneratorDirect",
            instructions=prompt_system_direct,
            model=model,
            output_type=CommitMessageOutput,
            model_settings=ModelSettings(include_usage=True)
        )
        result = await Runner.run(agent, user_content, max_turns=1)
        commit_message = result.final_output.body
        commit_title = result.final_output.subject

        usage = result.context_wrapper.usage
        total_usage["input"] = usage.input_tokens
        total_usage["cached"] = usage.input_tokens_details.cached_tokens
        total_usage["reasoning"] = usage.output_tokens_details.reasoning_tokens
        total_usage["output"] = usage.output_tokens
        total_usage["total"] = usage.total_tokens

    logger.info(f"Commit Agent Final Usage: {total_usage['total']} total tokens.")
    return commit_message, commit_title, total_usage["total"]


def split_chunks(content: str, max_size: int) -> List[str]:
    lines = content.splitlines(keepends=True)
    chunks, current_chunk_lines = [], []
    current_size = 0
    for line in lines:
        line_size = len(line.encode("utf-8"))
        if current_size + line_size > max_size and current_chunk_lines:
            chunks.append("".join(current_chunk_lines))
            current_chunk_lines = [line]
            current_size = line_size
        else:
            current_chunk_lines.append(line)
            current_size += line_size
    if current_chunk_lines:
        chunks.append("".join(current_chunk_lines))
    
    return chunks