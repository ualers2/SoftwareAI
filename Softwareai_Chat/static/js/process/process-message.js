function processMessageContent(text) {
  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, function (m) {
      return {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
      }[m];
    });
  }

  // Armazena blocos de código separados temporariamente
  const codeBlocks = [];
  text = text.replace(/```([\w+-]*)\n([\s\S]*?)```/g, function (_, lang, code) {
    const escapedCode = escapeHtml(code);
    const language = lang || 'plaintext';
    const id = 'code-' + Math.random().toString(36).substr(2, 9);
    const placeholder = `[[CODE_BLOCK_${codeBlocks.length}]]`;

    codeBlocks.push(`
      <div class="code-container relative group">
        <button class="copy-btn absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition" onclick="copyCode('${id}', this)">
          <div class="copy-wrapper">
            <span class="icon">
              <i class="fas fa-copy icon-copy"></i>
            </span>
            <span class="lang-label">${language}</span>
          </div>
        </button>
        <pre><code id="${id}" class="language-${language}">${escapedCode}</code></pre>
      </div>
    `);

    return placeholder;
  });

  // Código inline (fora dos blocos)
  text = text.replace(/`([^`]+)`/g, '<code>$1</code>');

  // Negrito / Itálico
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/\*([^*]+)\*/g, '<em>$1</em>');

  // Quebras de linha normais
  text = text.replace(/\n/g, '<br>');

  // Substitui os placeholders pelos blocos de código reais (sem <br>)
  codeBlocks.forEach((html, index) => {
    const placeholder = `[[CODE_BLOCK_${index}]]`;
    text = text.replace(placeholder, html);
  });

  return text;
}


function copyCode(id, btn) {
  const codeElement = document.getElementById(id);
  if (!codeElement) return;

  const plainText = codeElement.innerText;

  navigator.clipboard.writeText(plainText).then(() => {
    const iconSpan = btn.querySelector('.icon');
    iconSpan.innerHTML = `<i class="fas fa-check text-green-500 bg-gray-800 px-2 py-1 rounded-md"></i>`;
    
    btn.classList.add('copied');

    setTimeout(() => {
      iconSpan.innerHTML = `<i class="fas fa-copy text-sm text-white bg-gray-700 px-2 py-1 rounded-md"></i>`;
      btn.classList.remove('copied');
    }, 2000);
  }).catch(err => {
    console.error("Erro ao copiar:", err);
  });
}




// Scroll chat to bottom
function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

// Clear chat messages
function clearChat() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.innerHTML = '';
}

// Insert code block template
function insertCodeBlock() {
    const messageInput = document.getElementById('message-input');
    const currentValue = messageInput.value;
    const cursorPos = messageInput.selectionStart;
    
    const codeTemplate = "\n```python\n# Your code here\n```\n";
    const newValue = currentValue.substring(0, cursorPos) + codeTemplate + currentValue.substring(cursorPos);
    
    messageInput.value = newValue;
    messageInput.focus();
    
    // Position cursor inside the code block
    const newCursorPos = cursorPos + 12; // Position after "```python\n"
    messageInput.setSelectionRange(newCursorPos, newCursorPos);
  }
  