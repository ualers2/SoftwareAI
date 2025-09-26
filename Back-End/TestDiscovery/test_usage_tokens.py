from agents import Agent, ModelSettings, Runner
from dotenv import load_dotenv
import os
os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))


agent = Agent(
    name="Assistant",
    model_settings=ModelSettings(include_usage=True),
)

result = Runner.run_sync(agent, "What's the weather in Tokyo?")
print(result.context_wrapper.usage.total_tokens)