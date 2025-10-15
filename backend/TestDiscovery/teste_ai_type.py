
import json
import logging
import os
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Any, List, Optional, Union

import backoff
import openai
import pyperclip
from fastapi import WebSocket 
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chat_models.base import BaseChatModel
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    messages_from_dict,
    messages_to_dict,
)
from langchain_core.messages import (
    AIMessage,
    AnyMessage,
    BaseMessage,
    BaseMessageChunk,
    HumanMessage,
    convert_to_messages,
    convert_to_openai_image_block,
    is_data_content_block,
    message_chunk_to_message,
)
from langchain_anthropic import ChatAnthropic
from langchain_openai import AzureChatOpenAI, ChatOpenAI
from firebase_admin import App
from Agents.gpt_engineer.core.files_dict import FilesDict, file_to_lines_dict
from Agents.gpt_engineer.core.base_memory import BaseMemory

from Agents.gpt_engineer.core.default.steps import salvage_correct_hunks
from Agents.gpt_engineer.applications.cli.main import NonInteractiveFileSelector, memory_path, DiskMemory

# Type hint for a chat message
Message = Union[AIMessage, HumanMessage, SystemMessage]

def next(
    messages: List[Message],
) -> List[Message]:
    filename = "main.py"

    # with open(os.path.join(os.path.dirname(__file__), 'teste_main.diff'), 'r', encoding='utf-8') as f:
    #     diff = f.read()
    diff_content = """
--- main.py
+++ main.py
@@ -1,11 +1,11 @@
- def hello_world():
+ def hello_worlddddddddddddddd():
    print("Hello, World!")


def main():
    hello_world()


if __name__ == "__main__":
    main()
    
    """

    # print(f"diff {diff}")
    content_str = f"{diff_content}"
    response = BaseMessage(type="ai", content=content_str, filename=filename)
    content = response.content
    messages.append(response)
    return messages

def _improve(
    files_dict: FilesDict, 
    memory: BaseMemory, 
    messages: List, 
    repo_path='',
    diff_timeout=3
) -> FilesDict:
    messages = next(messages)
    files_dict, errors = salvage_correct_hunks(
        messages,
        files_dict,
        memory, 
        repo_path, 
        diff_timeout=diff_timeout
    )

    return files_dict, errors

# os.chdir(os.path.join(os.path.dirname(__file__)))

project_path=os.path.join(os.path.dirname(__file__), 'example8')

# mock files_dict 
file_selector = NonInteractiveFileSelector(project_path)
files_dict, is_linting = file_selector.ask_for_files(
    skip_file_selection=True
)
# print(f"files_dict.keys() {files_dict.keys()}")

# mock memory 
memory = DiskMemory(memory_path(project_path))
memory.archive_logs()

# mock messages 
messages = [
    SystemMessage(content="TESTE"),
]

# mock next 
messages = next(
    messages,
)

# mock improve 
files_dict, errors = _improve(
    files_dict, 
    memory, 
    messages, 
    repo_path=project_path,
    diff_timeout=3
)

print(f"errors {errors}")

# diff_content = messages[-1].content.strip()
# filename = messages[-1].filename
# print(f"filename {filename}")

# # Remove comentários do LLM
# cleaned_lines = [line for line in diff_content.splitlines() if not line.strip().startswith("//")]
# diff_content_cleaned = "\n".join(cleaned_lines)
# print(f"diff_content_cleaned {diff_content_cleaned}")
