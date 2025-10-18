from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import asyncio
import os
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "Keys", 'keys.env'))

import asyncio
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

current_dir = Path(__file__).parent
samples_dir = current_dir / "sample_files"

from agents import Agent, HostedMCPTool, Runner

async def gitmcp() -> None:
    agent = Agent(
        name="Assistant",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "gitmcp",
                    "server_url": "https://gitmcp.io/openai/codex",
                    "require_approval": "never",
                }
            )
        ],
    )

    result = await Runner.run(agent, "https://github.com/openai/openai-chatkit-advanced-samples Which language is this repository written in?")
    print(result.final_output)

# asyncio.run(gitmcp())


async def thinking() -> None:
    async with MCPServerStdio(
        name="sequential-thinking",
        params={
            "command": "docker",
            "args": [
                "run",
                "--rm",
                "-i",
                "mcp/sequentialthinking"
            ],
        },
        client_session_timeout_seconds=45
    ) as server:
        agent = Agent(
            name="Assistant",
            instructions="use o pensamento sequencial para responder o usuario",
            mcp_servers=[server],
        )
        result = await Runner.run(agent, "quanto é 900 divido por 7")
        print(result.final_output)

asyncio.run(thinking())