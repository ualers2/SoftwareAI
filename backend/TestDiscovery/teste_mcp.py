from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
import asyncio
import os
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "Keys", 'keys.env'))

import asyncio

from agents import Agent, HostedMCPTool, Runner

async def main() -> None:
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

asyncio.run(main())