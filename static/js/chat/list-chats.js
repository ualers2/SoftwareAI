async function loadAllChats() {
  try {
    console.log(localStorage.getItem('user_email'));
    const api_url_list_conversations = "https://softwareai.rshare.io/api/list-conversations";
    const response = await fetch(api_url_list_conversations, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_email: localStorage.getItem('user_email') })
    });

    if (!response.ok) throw new Error("Erro ao buscar lista de conversas");

    const conversations = await response.json();
    console.log("Conversas carregadas:", conversations);

    const chatHistoryElement = document.getElementById('chat-history');
    if (!chatHistoryElement) {
      console.error("Elemento #chat-history não encontrado no HTML");
      return;
    }

    chatHistoryElement.innerHTML = '';

    const activeSessionId = localStorage.getItem('session_id');

    conversations.forEach(conversation => {
      if (!Array.isArray(conversation.history) || conversation.history.length === 0) return;

      const item = document.createElement('div');
      item.className = 'chat-history-item p-2 rounded hover:bg-gray-800 cursor-pointer';
      if (conversation.session_id === activeSessionId) {
        item.classList.add('active');
      }

      const lastMessage = conversation.history[conversation.history.length - 1]?.content || "Nova conversa...";

      item.innerHTML = `
        <div class="text-sm font-medium truncate">${conversation.session_id}</div>
        <div class="text-xs text-gray-400 truncate">${lastMessage}</div>
      `;

      item.addEventListener('click', () => {
        localStorage.setItem('session_id', conversation.session_id);
        document.querySelectorAll('.chat-history-item').forEach(i => i.classList.remove('active'));
        item.classList.add('active');

        renderConversation(conversation);
      });

      chatHistoryElement.appendChild(item);
    });

    const firstConversation = conversations.find(c => c.session_id === activeSessionId) || conversations[0];
    if (firstConversation) {
      localStorage.setItem('session_id', firstConversation.session_id);
      renderConversation(firstConversation);
    }

  } catch (error) {
    console.error("Erro ao carregar lista de chats:", error);
  }
}

function renderConversation(conversation) {
  const container = document.getElementById('chat-messages'); // <- Atualizado!
  if (!container) {
    console.error('Elemento #chat-messages não encontrado!');
    return;
  }

  container.innerHTML = '';

  conversation.history.forEach(msg => {
    const div = document.createElement('div');
    const processedContent = processMessageContent(msg.content);

    let typeClass = '';
    let icon = '';
    let bgColor = '';
    let imageIcon = null; 

    if (msg.role === 'user') {
      typeClass = 'user-message';
      icon = 'fa-user';
      bgColor = 'gray';
    } else if (msg.role === 'agent') {
      bgColor = 'indigo';
      imageIcon = 'static/img/194397500.jpg';
    } else if (msg.role === 'assistant') {
      typeClass = 'agent-message';
      bgColor = 'indigo';
      imageIcon = 'static/img/194397500.jpg'; // Ícone do agente como imagem
    } else if (msg.role === 'system') {
      typeClass = 'system-message';
      bgColor = 'teal';
      imageIcon = 'static/img/194397500.jpg'; // Ícone do sistema como imagem
    }

    div.className = `chat-message ${typeClass} fade-in-up`;

    const iconHtml = imageIcon
      ? `<img src="${imageIcon}" class="w-8 h-8 rounded-md object-cover mr-4" alt="${msg.role}" />`
      : `<div class="w-8 h-8 rounded-md bg-${bgColor}-600 flex items-center justify-center text-white mr-4">
          <i class="fas ${icon}"></i>
        </div>`;

    div.innerHTML = `
      <div class="flex items-start">
        ${iconHtml}
        <div class="message-content">${processedContent}</div>
      </div>
    `;

    container.appendChild(div);
  });

  scrollToBottom();
  // Aplicar highlight.js ao recarregar mensagens antigas
  setTimeout(() => {
    document.querySelectorAll('pre code').forEach((block) => {
      hljs.highlightElement(block);
    });
  }, 0);


}


async function handleConversationItemClick(convo, clickedElement) {
  // Remove a classe 'active' de todos os itens e marca o clicado
  document.querySelectorAll('.chat-history-item').forEach(el => el.classList.remove('active'));
  if (clickedElement) clickedElement.classList.add('active');

  // Atualiza o session_id no localStorage
  localStorage.setItem('session_id', convo.session_id);

  // Limpa o chat atual
  clearChat();

  // Renderiza o histórico da conversa
  if (Array.isArray(convo.history)) {
    for (const message of convo.history) {
      if (message.role === 'user') {
        addMessage("user", message.content);
      } else if (message.role === 'assistant') {
        addMessage("agent", message.content);
      } else if (message.role === 'system') {
        addMessage("system", message.content);
      }
    }
    

    // Aguarda renderização antes de rolar
    setTimeout(scrollToBottom, 100);
  } else {
    console.warn("Histórico de conversa não encontrado ou inválido.");
  }
}
