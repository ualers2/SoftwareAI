async function loadConversation(sessionId) {

  try {
    console.log("Session ID enviado:", sessionId);

    const api_url_chat_conversation = "https://softwareai.rshare.io/api/chat-conversation";
    const response = await fetch(api_url_chat_conversation, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        session_id: sessionId,
        user_email: userEmail
      })
    });
  

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const conversation = await response.json();
    const chatHistoryElement = document.getElementById('chat-history');
    chatHistoryElement.innerHTML = '';

    const historyItem = document.createElement('div');
    historyItem.className = 'chat-history-item p-2 rounded hover:bg-gray-800 cursor-pointer';
    historyItem.innerHTML = `
      <div class="text-sm font-medium truncate">${conversation.session_id}</div>
      <div class="text-xs text-gray-400 truncate">${conversation.snippet}</div>
    `;

    historyItem.addEventListener('click', function () {
      handleConversationItemClick(conversation, historyItem);
    });

    chatHistoryElement.appendChild(historyItem);
  } catch (error) {
    console.error("Erro ao carregar a conversa:", error);
  }
}
