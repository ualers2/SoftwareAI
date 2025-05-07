// real_stream.js

let currentMessageElement = null;
let updateTimer = null;

// Buffer de texto bruto
let streamingBuffer = '';

function handleRealStream(payload) {
  const chunk = payload.message;

  // Cria o elemento na primeira vez
  if (!currentMessageElement) {
    streamingBuffer = '';  // zera buffer
    currentMessageElement = document.createElement('div');
    currentMessageElement.className = 'chat-message assistant-message fade-in-up';
    currentMessageElement.innerHTML = `
      <div class="flex items-start">
        <img src="static/img/194397500.jpg"
             class="w-8 h-8 rounded-md object-cover mr-4"
             alt="${payload.user}" />
        <div class="message-content">
          <span class="message-text"></span>
        </div>
      </div>
    `;
    document.getElementById('chat-messages').appendChild(currentMessageElement);
    currentMessageElement.scrollIntoView({ behavior: 'smooth' });
  }

  // Anexa o chunk ao buffer e ao elemento, sem processar
  streamingBuffer += chunk;
  currentMessageElement.querySelector('.message-text').textContent = streamingBuffer;

  // Garante que continue visível
  currentMessageElement.scrollIntoView({ behavior: 'smooth' });

  // Reinicia timer: se nada novo chegar em 5s, finaliza
  if (updateTimer) clearTimeout(updateTimer);
  updateTimer = setTimeout(() => {
    finalizeRealStream();
    updateTimer = null;
  }, 5000);
}

function finalizeRealStream() {
  if (!currentMessageElement) return;

  // Processa buffer completo para markdown e destaque de código
  const contentSpan = currentMessageElement.querySelector('.message-text');
  contentSpan.innerHTML = processMessageContent(streamingBuffer);
  currentMessageElement.querySelectorAll('pre code').forEach(block => {
    hljs.highlightElement(block);
  });

  // Zera estado
  currentMessageElement = null;
  streamingBuffer = '';
}
