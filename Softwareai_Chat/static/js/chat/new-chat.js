async function NewChat() {
  try {
    const userEmail = localStorage.getItem('user_email'); // guarde isso após login
    console.log(userEmail);

    const api_url_new_conversation = "https://softwareai.rshare.io/api/new-conversation";
    const response = await fetch(api_url_new_conversation, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: userEmail })
    });

    if (!response.ok) throw new Error("Erro ao criar nova conversa");

    const conversation = await response.json();
    const newSessionId = conversation.session_id;
    localStorage.setItem('session_id', newSessionId);


    // ✅ Mensagens de sistema
    addMessage('system', '💬 New conversation started successfully.');
    if (window.active_agent_slug) {
      addMessage('system', `🤖 The ${window.active_agent_name} agent is ready to help you!`);
    }

    // ❌ Remove "active" anterior
    document.querySelectorAll('.chat-history-item').forEach(item => {
      item.classList.remove('active');
    });

    // ➕ Cria novo item na sidebar
    const chatHistoryElement = document.getElementById('chat-history');
    const newItem = document.createElement('div');
    newItem.className = 'chat-history-item p-2 rounded hover:bg-gray-800 cursor-pointer active';
    newItem.innerHTML = `
      <div class="text-sm font-medium truncate">${newSessionId}</div>
      <div class="text-xs text-gray-400 truncate">Nova conversa...</div>
    `;
    newItem.addEventListener('click', () => {
      handleConversationItemClick(conversation, newItem);
    });

    chatHistoryElement.appendChild(newItem);

    return newSessionId; // ✅ retorna o ID da sessão

  } catch (err) {
    console.error("Erro ao iniciar nova conversa:", err);
  }

}
// document.getElementById('new-chat').addEventListener('click', async () => {
  
// });
  

