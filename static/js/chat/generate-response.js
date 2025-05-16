function clearAllAttachedFiles() {
    console.log("🧹 Limpando todos os arquivos anexados...");
    window.selectedFiles = [];
    renderAttachedFiles();
}
function clearAllAttachedImages() {
    console.log("🧹 Limpando todas as imagens anexadas...");
    window.selectedImages = [];
    renderImagePreviews(); // supondo que essa função exista
}
  
function showTypingIndicator() {
    // Evita adicionar múltiplos indicadores
    if (document.getElementById('typing-indicator')) return;

    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.createElement('div');
    typingIndicator.id = 'typing-indicator';
    typingIndicator.className = 'chat-message agent-message';

    typingIndicator.innerHTML = `
        <div class="flex items-start">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;

    chatMessages.appendChild(typingIndicator);
    scrollToBottom();
}

// Remove typing indicator
function removeTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

async function generateResponse(message) {
    // Verifica se há um agente ativo com slug definido
    const activeAgentSlug = window.active_agent_slug;
    const api_url_post = activeAgentSlug
        ? `https://softwareai.rshare.io/api/response-conversation/${activeAgentSlug}`
        : `https://softwareai.rshare.io/api/response-conversation`;

    const sessionId = getSessionId();
    const userEmail = localStorage.getItem('user_email');
    const messageInput = document.getElementById('message-input');

    const apitoken = document.getElementById('api-token');
    const apiKey = apitoken.innerText.replace('API TOKEN: ', '').trim();

    const formData = new FormData();
    formData.append('message', message);
    formData.append('session_id', sessionId);
    formData.append('user_email', userEmail);
    formData.append('apiKey', apiKey);
    // formData.append('key_openai', ApiKeyInput);
    
    // Adiciona arquivos e imagens já selecionados por outros métodos
    window.selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    window.selectedImages.forEach(image => {
        formData.append('images', image);
    });


    // Finaliza a mensagem atual, se houver, para evitar atualizações no bloco anterior
    finalizeAgentMessage();
    
    // Adiciona a mensagem do usuário à interface
    addMessage("user", message);

    // Limpa o campo de input
    messageInput.value = '';

    // Exibe o indicador de digitação
    showTypingIndicator();
     
    try {
        const response = await fetch(api_url_post, {
            method: 'POST',
            body: formData, 
            headers: {
                'X-API-KEY': apiKey
            }
        });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        window.selectedFiles = [];
        window.selectedImages = [];
        renderAttachedFiles();
        renderImagePreviews();
        
        console.log("Mensagem enviada com sucesso para o webhook");
    } catch (error) {
        console.error("Erro ao enviar mensagem para o webhook:", error);
    }
}
