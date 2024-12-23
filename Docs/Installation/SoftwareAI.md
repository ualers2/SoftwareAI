
### Installation SoftwareAI
```bash
git clone https://github.com/ualers/SoftwareAI
```
### Installation requirements
```bash
pip install -r requirements.txt
```
### Basic Usage
```python
# Importing SoftwareAI Agents
from CoreApp._init_agents_ import AgentInitializer

# Importing SoftwareAI Libraries
from CoreApp._init_libs_ import *

# Initializing Agent
byte_manager = AgentInitializer.get_agent('ByteManager') 

# Usage Example
message = "I request a script for technical analysis of Solana cryptocurrency"
owner_response = byte_manager.AI_1_ByteManager_Company_Owners(message)
print(owner_response)
```

## 💡 Features
- 📊 Creation of pre-project documentation
- 🗺️ Roadmap generation
- 📅 Automatic schedules
- 📝 Requirements analysis
- 🔄 GitHub repository management
- ⚡ Loop of 5 automatic improvements
- 📚 Repository on github generated with the example above: https://github.com/A-I-O-R-G/solana-analyzer
#