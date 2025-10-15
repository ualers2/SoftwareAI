"""
Fixed non-interactive CLI implementation
This removes ALL interactive elements and makes it truly returnable.
"""
import time
import difflib
import json
import logging
from datetime import datetime
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from fastapi import WebSocket 
import openai
from dotenv import load_dotenv
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from termcolor import colored
from firebase_admin import App, db

# Import your existing modules
from Agents.gpt_engineer.applications.cli.cli_agent import CliAgent
from Agents.gpt_engineer.applications.cli.file_selector import FileSelector
from Agents.gpt_engineer.core.ai import AI
from Agents.gpt_engineer.core.default.disk_execution_env import DiskExecutionEnv
from Agents.gpt_engineer.core.default.disk_memory import DiskMemory
from Agents.gpt_engineer.core.default.file_store import FileStore
from Agents.gpt_engineer.core.default.paths import PREPROMPTS_PATH, memory_path
from Agents.gpt_engineer.core.default.steps import (
    execute_entrypoint,
    gen_code,
    handle_improve_mode,
    improve_fn as improve_fn,
)
from Agents.gpt_engineer.core.files_dict import FilesDict
from Agents.gpt_engineer.core.git import stage_uncommitted_to_git
from Agents.gpt_engineer.core.preprompts_holder import PrepromptsHolder
from Agents.gpt_engineer.core.prompt import Prompt
from Agents.gpt_engineer.tools.custom_steps import clarified_gen, lite_gen, self_heal
# from modules.Chat.history.save_history_user import save_history_user
# from modules.Chat.history.save_history_system import save_history_system

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main_logger")

class GPTEngineerResult:
    """Class to hold the results of GPT Engineer execution."""
    
    def __init__(self, 
                 success: bool = False,
                 files_dict: Optional[FilesDict] = None,
                 error_message: Optional[str] = None,
                 changes_made: bool = False,
                 token_usage: Optional[Dict[str, Any]] = None,
                 system_info: Optional[Dict[str, Any]] = None,
                 diff_output: Optional[str] = None):
        self.success = success
        self.files_dict = files_dict
        self.error_message = error_message
        self.changes_made = changes_made
        self.token_usage = token_usage
        self.system_info = system_info
        self.diff_output = diff_output
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            'success': self.success,
            'files_dict': self.files_dict.to_dict() if self.files_dict else None,
            'error_message': self.error_message,
            'changes_made': self.changes_made,
            'token_usage': self.token_usage,
            'system_info': self.system_info,
            'diff_output': self.diff_output
        }


class NonInteractiveFileSelector:
    """Non-interactive version of FileSelector that doesn't prompt user."""
    
    def __init__(self, project_path: str):
        self.project_path = project_path
    
    def ask_for_files(self, skip_file_selection: bool = True) -> Tuple[FilesDict, bool]:
        """Non-interactive file selection - returns all relevant files."""
        files_dict = FilesDict()
        project_path = Path(self.project_path)
        
        # Extensões de arquivos de código, incluindo React/Vite
        code_extensions = {
            '.py', '.js', '.jsx', '.ts', '.tsx', '.mjs', '.cjs',
            '.html', '.css', '.json', '.txt', '.md',
            '.yml', '.yaml', '.toml', '.env', '.gitignore'
        }
        
        for file_path in project_path.rglob('*'):
            if (
                file_path.is_file() and
                file_path.suffix.lower() in code_extensions and
                not any(part.startswith('.') for part in file_path.parts) and
                'node_modules' not in file_path.parts and
                '__pycache__' not in file_path.parts
            ):
                try:
                    relative_path = file_path.relative_to(project_path)
                    with file_path.open('r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    files_dict[str(relative_path)] = content
                except Exception as e:
                    print(f"Warning: Could not read {file_path}: {e}")
        
        # False indica que não é só linters, mas uso normal
        return files_dict, False

def load_env_if_needed():
    """Load environment variables if the OPENAI_API_KEY is not already set."""
    if os.getenv("OPENAI_API_KEY") is None:
        load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None:
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

    openai.api_key = os.getenv("OPENAI_API_KEY")

    if os.getenv("ANTHROPIC_API_KEY") is None:
        load_dotenv()
    if os.getenv("ANTHROPIC_API_KEY") is None:
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))


def concatenate_paths(base_path, sub_path):
    """Compute the relative path from base_path to sub_path."""
    relative_path = os.path.relpath(sub_path, base_path)
    if not relative_path.startswith(".."):
        return sub_path
    return os.path.normpath(os.path.join(base_path, sub_path))


def load_prompt_non_interactive(
    input_repo: DiskMemory,
    improve_mode: bool,
    prompt_file: str,
    image_directory: str,
    entrypoint_prompt_file: str = "",
    default_prompt: str = "",
    default_improve_prompt: str = ""
) -> Prompt:
    """Load prompt from file or use default prompts (non-interactive version)."""
    
    if os.path.isdir(prompt_file):
        raise ValueError(
            f"The path to the prompt, {prompt_file}, already exists as a directory. "
            "No prompt can be read from it. Please specify a prompt file using --prompt_file"
        )
    
    prompt_str = input_repo.get(prompt_file)
    if prompt_str:
        print(colored("Using prompt from file:", "green"), prompt_file)
        print(prompt_str)
    else:
        if not improve_mode:
            if not default_prompt:
                raise ValueError(
                    "No prompt file found and no default_prompt provided. "
                    "Please provide a prompt file or default_prompt parameter."
                )
            prompt_str = default_prompt
            print(colored("Using default prompt:", "yellow"))
            print(prompt_str)
        else:
            if not default_improve_prompt:
                raise ValueError(
                    "No prompt file found and no default_improve_prompt provided. "
                    "Please provide a prompt file or default_improve_prompt parameter."
                )
            prompt_str = default_improve_prompt
            print(colored("Using default improve prompt:", "yellow"))
            print(prompt_str)

    if entrypoint_prompt_file == "":
        entrypoint_prompt = ""
    else:
        full_entrypoint_prompt_file = concatenate_paths(
            input_repo.path, entrypoint_prompt_file
        )
        if os.path.isfile(full_entrypoint_prompt_file):
            entrypoint_prompt = input_repo.get(full_entrypoint_prompt_file)
        else:
            raise ValueError("The provided file at --entrypoint-prompt does not exist")

    if image_directory == "":
        return Prompt(prompt_str, entrypoint_prompt=entrypoint_prompt)

    full_image_directory = concatenate_paths(input_repo.path, image_directory)
    if os.path.isdir(full_image_directory):
        if len(os.listdir(full_image_directory)) == 0:
            raise ValueError("The provided --image_directory is empty.")
        image_repo = DiskMemory(full_image_directory)
        return Prompt(
            prompt_str,
            image_repo.get(".").to_dict(),
            entrypoint_prompt=entrypoint_prompt,
        )
    else:
        raise ValueError("The provided --image_directory is not a directory.")


def get_preprompts_path(use_custom_preprompts: bool, input_path: Path) -> Path:
    """Get the path to the preprompts, using custom ones if specified."""
    original_preprompts_path = PREPROMPTS_PATH
    if not use_custom_preprompts:
        return original_preprompts_path

    custom_preprompts_path = input_path / "preprompts"
    if not custom_preprompts_path.exists():
        custom_preprompts_path.mkdir()

    for file in original_preprompts_path.glob("*"):
        if not (custom_preprompts_path / file.name).exists():
            (custom_preprompts_path / file.name).write_text(file.read_text())
    return custom_preprompts_path


def compare_files(f1: FilesDict, f2: FilesDict) -> str:
    """Compare two FilesDict objects and return diff as string."""
    def colored_diff(s1, s2):
        lines1 = s1.splitlines()
        lines2 = s2.splitlines()
        diff = difflib.unified_diff(lines1, lines2, lineterm="")
        
        RED = "\033[38;5;202m"
        GREEN = "\033[92m"
        RESET = "\033[0m"
        
        colored_lines = []
        for line in diff:
            if line.startswith("+"):
                colored_lines.append(GREEN + line + RESET)
            elif line.startswith("-"):
                colored_lines.append(RED + line + RESET)
            else:
                colored_lines.append(line)
        
        return "\n".join(colored_lines)

    diff_output = []
    for file in sorted(set(f1) | set(f2)):
        diff = colored_diff(f1.get(file, ""), f2.get(file, ""))
        if diff:
            diff_output.append(f"Changes to {file}:")
            diff_output.append(diff)
    
    return "\n".join(diff_output)


def get_system_info() -> Dict[str, Any]:
    """Get system information for debugging."""
    system_info = {
        "os": platform.system(),
        "os_version": platform.version(),
        "architecture": platform.machine(),
        "python_version": sys.version,
        "packages": format_installed_packages(get_installed_packages()),
    }
    return system_info


def get_installed_packages():
    """Get installed Python packages."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
        )
        packages = json.loads(result.stdout)
        return {pkg["name"]: pkg["version"] for pkg in packages}
    except Exception as e:
        return str(e)


def format_installed_packages(packages):
    """Format installed packages for display."""
    if isinstance(packages, str):
        return packages
    return "\n".join([f"{name}: {version}" for name, version in packages.items()])


# Non-interactive execution function that doesn't prompt
def non_interactive_execute_entrypoint(ai, execution_env, files_dict, **kwargs):
    """Non-interactive version that doesn't ask for user input."""
    print("Skipping execution confirmation in non-interactive mode")
    return files_dict


def run_gpt_engineer(
    project_path: str = ".",
    model: str = None,
    temperature: float = 0.1,
    improve_mode: bool = False,
    lite_mode: bool = False,
    clarify_mode: bool = False,
    self_heal_mode: bool = False,
    azure_endpoint: str = "",
    use_custom_preprompts: bool = False,
    llm_via_clipboard: bool = False,
    verbose: bool = False,
    debug: bool = False,
    prompt_file: str = "prompt",
    entrypoint_prompt_file: str = "",
    image_directory: str = "",
    use_cache: bool = False,
    skip_file_selection: bool = True,
    no_execution: bool = False,
    diff_timeout: int = 3,
    default_prompt: str = "",
    default_improve_prompt: str = "",
    auto_apply_changes: bool = True,
    return_system_info: bool = False,
    skip_entrypoint_execution: bool = True,
    WebSocketFlag: Optional[WebSocket] = None,
    session_id: Optional[str] = None,
    user_email: Optional[str] = None,
    appcompany: Optional[App] = None,
) -> GPTEngineerResult:
    """
    Non-interactive version of the main GPT Engineer function.
    
    Parameters
    ----------
    skip_entrypoint_execution : bool
        If True, skips the execution step that asks for user confirmation
    
    Returns
    -------
    GPTEngineerResult
        Object containing the results of the operation.
    """
    
    try:
        # save_history_user(session_id, user_email, default_prompt, appcompany)


        # Set model default
        if model is None:
            model = os.environ.get("MODEL_NAME", "gpt-4o")
        
        # Return system info if requested
        if return_system_info:
            sys_info = get_system_info()
            return GPTEngineerResult(
                success=True,
                system_info=sys_info
            )

        # Validate arguments
        if improve_mode and (clarify_mode or lite_mode):
            return GPTEngineerResult(
                success=False,
                error_message="Error: Clarify and lite mode are not compatible with improve mode."
            )

        # Set up logging
        logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)
        if use_cache:
            set_llm_cache(SQLiteCache(database_path=".langchain.db"))

        load_env_if_needed()

        if WebSocketFlag == None:
            ai = AI(
                model_name=model,
                temperature=temperature,
                azure_endpoint=azure_endpoint,
                ActiveWebSocket=None
            )
        else:
            ai = AI(
                model_name=model,
                temperature=temperature,
                azure_endpoint=azure_endpoint,
                ActiveWebSocket=WebSocketFlag,
                session_id=session_id,
                user_email=user_email,
                appcompany=appcompany,
            )

        path = Path(project_path)
        print("Running gpt-engineer in", path.absolute(), "\n")


        # Load prompt (non-interactive version)
        prompt = load_prompt_non_interactive(
            DiskMemory(path),
            improve_mode,
            prompt_file,
            image_directory,
            entrypoint_prompt_file,
            default_prompt,
            default_improve_prompt
        )

        if not ai.vision:
            prompt.image_urls = None

        # Configure generation function
        if clarify_mode:
            code_gen_fn = clarified_gen
        elif lite_mode:
            code_gen_fn = lite_gen
        else:
            code_gen_fn = gen_code

        # Configure execution function - use non-interactive version
        if skip_entrypoint_execution:
            execution_fn = non_interactive_execute_entrypoint
        elif self_heal_mode:
            execution_fn = self_heal
        else:
            execution_fn = execute_entrypoint

        preprompts_holder = PrepromptsHolder(
            get_preprompts_path(use_custom_preprompts, Path(project_path))
        )

        memory = DiskMemory(memory_path(project_path))
        memory.archive_logs()

        execution_env = DiskExecutionEnv()
        agent = CliAgent.with_default_config(
            memory,
            execution_env,
            ai=ai,
            code_gen_fn=code_gen_fn,
            improve_fn=improve_fn,
            process_code_fn=execution_fn,
            preprompts_holder=preprompts_holder,
            repo_path=project_path
        )

        files = FileStore(project_path)
        files_dict = None
        diff_output = None
        changes_made = False

        if not no_execution:
            if improve_mode:
                # Use non-interactive file selector
                file_selector = NonInteractiveFileSelector(project_path)
                files_dict_before, is_linting = file_selector.ask_for_files(
                    skip_file_selection=skip_file_selection
                )

                # Lint the code
                if is_linting:
                    files_dict_before = files.linting(files_dict_before)

                files_dict = handle_improve_mode(
                    prompt, agent, memory, files_dict_before, diff_timeout=diff_timeout
                )
                
                if not files_dict or files_dict_before == files_dict:
                    return GPTEngineerResult(
                        success=False,
                        error_message=f"No changes applied. Debug log available in {memory.path}/logs folder"
                    )
                else:
                    diff_output = compare_files(files_dict_before, files_dict)
                    changes_made = True
                    
                    if not auto_apply_changes:
                        # Return the diff for manual review
                        return GPTEngineerResult(
                            success=True,
                            files_dict=files_dict,
                            changes_made=changes_made,
                            diff_output=diff_output,
                            token_usage="0"
                        )

            else:
                files_dict = agent.init(prompt)
                changes_made = True

            # Apply changes
            stage_uncommitted_to_git(path, files_dict, improve_mode)
            files.push(files_dict)

        return GPTEngineerResult(
            success=True,
            files_dict=files_dict,
            changes_made=changes_made,
            token_usage="0",
            diff_output=diff_output
        )

    except Exception as e:
        if debug:
            import traceback
            traceback.print_exc()
        
        return GPTEngineerResult(
            success=False,
            error_message=str(e)
        )


def _get_token_usage(ai) -> Dict[str, Any]:
    """Helper function to get token usage information."""
    try:
        if hasattr(ai, 'token_usage_log'):
            if ai.token_usage_log.is_openai_model():
                return {
                    'cost': ai.token_usage_log.usage_cost(),
                    'type': 'openai'
                }
            elif os.getenv("LOCAL_MODEL"):
                return {
                    'cost': 0.0,
                    'type': 'local'
                }
            else:
                return {
                    'total_tokens': ai.token_usage_log.total_tokens(),
                    'type': 'other'
                }
    except Exception:
        pass
    return {'type': 'unknown'}


# # Simple test script
# if __name__ == "__main__":
#     # Test the non-interactive function
#     result = run_gpt_engineer(
#         project_path="./my_project",
#         default_prompt="Create a simple web server using Flask",
#         model="gpt-4o",
#         auto_apply_changes=True,
#         skip_entrypoint_execution=True,
#         verbose=True
#     )
    
#     print("\n" + "="*50)
#     print("RESULT:")
#     print("="*50)
    
#     if result.success:
#         print("✅ GPT Engineer completed successfully")
#         print(f"📁 Changes made: {result.changes_made}")
        
#         if result.files_dict:
#             print(f"📄 Generated files:")
#             for filename in result.files_dict.keys():
#                 print(f"  - {filename}")
        
#         if result.token_usage:
#             if result.token_usage['type'] == 'openai':
#                 print(f"💰 Total API cost: ${result.token_usage.get('cost', 'unknown')}")
#             elif result.token_usage['type'] == 'local':
#                 print("💰 Total API cost: $0.0 (using local LLM)")
#             else:
#                 print(f"🔢 Total tokens used: {result.token_usage.get('total_tokens', 'unknown')}")
        
#         if result.diff_output:
#             print("\n📝 Changes made:")
#             print(result.diff_output)
            
#     else:
#         print(f"❌ GPT Engineer failed: {result.error_message}")
    
#     print("\nResult object:", result.to_dict())