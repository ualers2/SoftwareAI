
  
// Handle sending a new message
function handleSendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
  
    if (!message) return;

    // Envia a mensagem para o backend
    generateResponse(message);
  }

// Limpa a referência da mensagem do agente após a resposta completa
function finalizeAgentMessage() {
    currentMessageElement = null;
}
  
// Add welcome message from the agent
function addWelcomeMessage() {
  const chatMessages = document.getElementById('chat-messages');
  // Get the current agent name for a personalized greeting
  const agentNameElement = document.querySelector('#agent-header h1');
  const agentName = agentNameElement ? agentNameElement.textContent : 'AI Assistant';
  
  const welcomeMessage = `
      <div class="chat-message agent-message">
          <div class="flex items-start">
              <div class="w-8 h-8 rounded-md bg-blue-600 flex items-center justify-center text-white mr-4">
                  <i class="fas fa-robot"></i>
              </div>
              <div class="message-content">
                  <p class="text-gray-100 mb-2">Hello! I'm ${agentName}. How can I assist you today?</p>
              </div>
          </div>
      </div>
  `;
  chatMessages.innerHTML = welcomeMessage;
  scrollToBottom();
}

// // Variável global para armazenar o timer de finalização
// let updateTimer = null;

// // Atualiza progressivamente a mensagem do agente
// function updateAgentMessage(newText) {
//   if (!currentMessageElement) {
//       // Se não existe um elemento, cria um novo para a mensagem progressiva
//       currentMessageElement = document.createElement('div');
//       currentMessageElement.className = 'chat-message agent-message';
//       currentMessageElement.innerHTML = `
//           <div class="flex items-start">
//               <div class="w-8 h-8 rounded-md bg-blue-600 flex items-center justify-center text-white mr-4">
//                   <i class="fas fa-robot"></i>
//               </div>
//               <div class="message-content"><span class="message-text"></span></div>
//           </div>
//       `;
//       document.getElementById('chat-messages').appendChild(currentMessageElement);
//       scrollToBottom();
//   }
  
//   const processed = processMessageContent(newText);
//   currentMessageElement.querySelector('.message-text').innerHTML = processed;
  
//   // Aplicar highlight.js ao novo conteúdo
//   setTimeout(() => {
//     currentMessageElement.querySelectorAll('pre code').forEach((block) => {
//       hljs.highlightElement(block);
//     });
//   }, 0);
  
//   // Reinicia o timer de finalização: se nenhuma atualização for recebida em 1 segundo, finaliza a mensagem
//   if (updateTimer) clearTimeout(updateTimer);
//   updateTimer = setTimeout(() => {
//     finalizeAgentMessage();
//     updateTimer = null;
//   }, 300000); // Ajuste o tempo conforme necessário
// }
