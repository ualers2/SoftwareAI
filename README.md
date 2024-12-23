
![UI](Gifs/logo.gif)
# 👥 Your software company governed by AI
![Version](https://img.shields.io/badge/version-0.2.8-blue)
![Status](https://img.shields.io/badge/status-beta-yellow)
![License](https://img.shields.io/badge/license-Apache-green)

# 📜 Table of Contents
- [📖 About](Docs/About/SoftwareAI.md)
- [📖 Index Docs](#-indexdocs)
- [🔄 Info-Update](Docs/Update/Update.md)
- [🚀 Starting SoftwareAI Chat](#-start-softwareai-chat)
- [🚀 Starting SoftwareAI Editor](#-softwareai-editor)
- [🚀 Starting Without Ui](#-get-started-softwareai-without-ui)
- [👥 Index-Team](Docs/IndexTeam/IndexTeam.md)
- [🗺️ Roadmaps](Docs/Roadmaps)
- [📊 Flowchart](Docs/Flowchart/Fluxogram-beta-v-0.1.8.pdf)
- [📁 SoftwareAI Structure](Docs/Structure/SoftwareAIStructure.md)
- [🤝 Contributing](#-contributing)
#

⚠️ **Note**: SoftwareAI is in beta phase and does not currently reflect the final product.
## 🚀 SoftwareAI-Editor 
**Build Agents**: Edit, Build and Bring your Agent to life
![UI](Gifs/1222.gif)
📖 **SoftwareAI-Editor**: is the most important part when thinking about creating a company 100% governed by AI, here we will build and modify each agent for its specific use
## 📚 [Editor Installation](Docs/Installation/Editor.md)
## 📚 [Editor RoadMap](Docs/Roadmaps/Editor-Roadmap.md)
#

#

## 🚀 Start SoftwareAI-Chat
⚠️ **Note**: It is with great pleasure that we present a functional version of the softwareai chat, now you can select the agent and chat with him with images, files and messages (audio coming soon) in addition, inspired by the openai whiteboard we created our own whiteboard where all generated code goes for her, despite being very complete there is still a lot to be done if you find an error open an Issues
![UI](Gifs/1221.gif)

## 📚 [SoftwareAI-Chat Installation](Docs/Installation/Chat.md)
## 📚 [SoftwareAI-Chat RoadMap](Docs/Roadmaps/Chat-Roadmap.md)
#
## 🚀 Get started SoftwareAI without UI
- 🔧 [SoftwareAI Installation](Docs/Installation/SoftwareAI.md)
- 🔧 Basic Usage:
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
## 💡 SoftwareAI without UI Features
- 📊 Creation of pre-project documentation
- 🗺️ Roadmap generation
- 📅 Automatic schedules
- 📝 Requirements analysis
- 🔄 GitHub repository management
- ⚡ Loop of 5 automatic improvements
- 📚 Repository on github generated with the example above: https://github.com/A-I-O-R-G/solana-analyzer


## 📖 IndexDocs
- [About](Docs/About)
- [Core](Docs/Core)
- [Destilation](Docs/Destilation/DestilationAgents.md)
- [IndexTeam](Docs/IndexTeam/IndexTeam.md)
- [Installation](Docs/Installation)
- [Moderation](Docs/Moderation/RemoveWords.md)
- [Roadmaps](Docs/Roadmaps)
- [Structure](Docs/Structure/SoftwareAIStructure.md)
- [ToolsAndFunctions](Docs/ToolsAndFunctions/doc-tools.md)
- [Update](Docs/Update/Update.md)
## 🤝 Contributing
While SoftwareAI is primarily AI-driven, we welcome contributions from the community:
- 🐛 Bug Reports
- 💡 Feature Suggestions
- 📝 Documentation Improvements
- 🔧 Code Contributions


