## 📖 Chat Roadmap
## **Chat**  
- **21/12/2024**  
  - [X] `Whiteboard` for code integrated into chat made in QCustomCodeEditor
  - [X] `ResponseAgent_message_with_assistants` with new argument `streamLoggerCode: Optional[Signal] = None,` made to support QCustomCodeEditor during the stream 
  - [X] Regex for bash interpreter `Chat/Formatmessage`
  - [X] `QCustomPerlinLoader` added to display loading messages from `Chat/QReadOpenAI` and `Chat/QListAgent`
  - [X] `ignore_python_code` added to hide the code already displayed on the board, preventing it from appearing in Qtextedit
  - [X] `closeEvent` added to stop Chat QThreads