function addMessage(type, content) {
    const message = document.createElement('div');
    message.className = `chat-message ${type}-message fade-in-up`;
  
    // Process message for markdown and code highlighting
    const processedcontent = processMessageContent(content);

    let icon = 'fa-user';
    let bgColor = 'gray';
    let imageIcon = null;
  
    if (type === 'agent') {
      bgColor = 'indigo';
      imageIcon = 'static/img/194397500.jpg';
    } else if (type === 'system') {
      bgColor = 'indigo';
      imageIcon = 'static/img/194397500.jpg';
    }
    else if (type === 'assistant') {
      bgColor = 'indigo';
      imageIcon = 'static/img/194397500.jpg'; // Ícone do agente como imagem
    }    
    const iconHtml = imageIcon
      ? `<img src="${imageIcon}" class="w-8 h-8 rounded-md object-cover mr-4" alt="${type}" />`
      : `<div class="w-8 h-8 rounded-md bg-${bgColor}-600 flex items-center justify-center text-white mr-4">
          <i class="fas ${icon}"></i>
        </div>`;
  
    message.innerHTML = `
      <div class="flex items-start">
        ${iconHtml}
        <div class="message-content">${processedcontent}</div>
      </div>
    `;
  
    document.getElementById('chat-messages').appendChild(message);
  
    message.scrollIntoView({ behavior: 'smooth' });
    // Aplicar highlight.js
    message.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightElement(block);
    });
}
  
