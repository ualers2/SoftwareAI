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
        model = "gpt-5-nano",
        MAX_INPUT_SIZE: int = 40000,
    ):
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    diff_size = len(diff.encode("utf-8"))
    logger.info(f"Commit Agent - Diff size (bytes): {diff_size}")

    total_usage = {
        "input": 0, "cached": 0, "reasoning": 0, "output": 0, "total": 0
    }

    if diff_size > MAX_INPUT_SIZE:
        logger.info(f"Diff exceeds {MAX_INPUT_SIZE} bytes. Initiating chunking process.")
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
        """
        chunks = split_chunks(diff, MAX_INPUT_SIZE)
        logger.info(f"Diff split into {len(chunks)} chunks.")
        summaries = []
        for i, chunk in enumerate(chunks, 1):
            chunk_content = f"""
            Analyzing chunk {i}/{len(chunks)} of a large diff.
            Modified files for context: {", ".join(files[:10])}{"..." if len(files) > 10 else ""}
            
            Diff Chunk:
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

        combined_summary = f"""
        Context:
        - Modified files: {", ".join(files)}

        Aggregated summaries from all diff chunks:
        ---
        {chr(10).join(summaries)}
        ---
        Please synthesize this information into the final commit message.
        """
        
        agent_summarizer = Agent(
            name="CommitSummarizer",
            instructions=prompt_final_summarizer,
            model=model,
            output_type=CommitMessageOutput,
            model_settings=ModelSettings(include_usage=True)
        )
        result = await Runner.run(agent_summarizer, combined_summary, max_turns=1)
        commit_message = result.final_output

        usage = result.context_wrapper.usage
        total_usage["input"] += usage.input_tokens
        total_usage["cached"] += usage.input_tokens_details.cached_tokens
        total_usage["reasoning"] += usage.output_tokens_details.reasoning_tokens
        total_usage["output"] += usage.output_tokens
        total_usage["total"] += usage.total_tokens

    else:
        
        logger.info("Diff size is within limits. Using direct processing.")
        
        prompt_system_direct = f"""
        You are a Git expert tasked with writing clear, informative commit messages.
        Analyze the provided code changes (diff) and the list of modified files.
        Your output MUST be a valid JSON object conforming to the `CommitMessageOutput` schema, with:
        - 'subject': A concise, imperative line (max 72 chars).
        - 'body': A detailed explanation of the 'what' and 'why' of the change.
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
        
        agent = Agent(
            name="CommitMessageGeneratorDirect",
            instructions=prompt_system_direct,
            model=model,
            output_type=CommitMessageOutput,
            model_settings=ModelSettings(include_usage=True)
        )
        result = await Runner.run(agent, user_content, max_turns=1)
        commit_message = result.final_output

        usage = result.context_wrapper.usage
        total_usage["input"] = usage.input_tokens
        total_usage["cached"] = usage.input_tokens_details.cached_tokens
        total_usage["reasoning"] = usage.output_tokens_details.reasoning_tokens
        total_usage["output"] = usage.output_tokens
        total_usage["total"] = usage.total_tokens

    logger.info(f"Commit Agent Final Usage: {total_usage['total']} total tokens.")
    return commit_message, total_usage["input"], total_usage["cached"], total_usage["output"], total_usage["reasoning"], total_usage["total"]


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