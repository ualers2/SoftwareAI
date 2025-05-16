function initChatUI() {
  // Obter elementos da interface
  const messageInput = document.getElementById('message-input');
  const sendButton = document.getElementById('send-message');
  const uploadImage = document.getElementById('upload-image');
  const fileUpload = document.getElementById('file-upload');
  const uploadButton = document.getElementById('upload-file');
  const attachedFiles = document.getElementById('attached-files');
  const imagePreviews = document.getElementById('image-previews');
  const imageUpload = document.getElementById('image-upload');
  const settingsButton = document.getElementById('settings-button');
  const settingsButton2 = document.getElementById('settings-button2');
  
  const settingsModal = document.getElementById('settings-modal');
  const closeSettings = document.getElementById('close-settings');
  const newChatButton = document.getElementById('new-chat');
  const connectfirebase = document.getElementById('connect-firebase');
  
  messageInput.value = '';

  // Configuração do highlight.js para sintaxe de código
  hljs.configure({
    languages: ['javascript', 'python', 'html', 'css', 'typescript', 'jsx', 'tsx', 'bash']
  });

  
  window.selectedFiles = [];
  window.selectedImages = [];

  // 📸 Upload de imagem
  function handleImageUpload() {
    const files = Array.from(imageUpload.files);
    window.selectedImages = files;
    renderImagePreviews();
  }
  

  uploadImage.addEventListener('click', function () {
    imageUpload.click(); // Abre a caixa de seleção
  });

  imageUpload.addEventListener('change', handleImageUpload);

  imagePreviews.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-image')) {
      const index = parseInt(e.target.dataset.index);
      window.selectedImages.splice(index, 1);
      renderImagePreviews();
    }
  });

  // 📎 Upload de arquivos
  uploadButton.addEventListener('click', () => {
    fileUpload.click();
  });

  fileUpload.addEventListener('change', () => {
    const files = Array.from(fileUpload.files);
    window.selectedFiles = files;
    renderAttachedFiles();
  });

  attachedFiles.addEventListener('click', (e) => {
    if (e.target.classList.contains('remove-file')) {
      const index = parseInt(e.target.dataset.index);
      window.selectedFiles.splice(index, 1);
      renderAttachedFiles();
    }
  });

  function getSCIAMode() {
    const selected = document.querySelector('input[name="scia-mode"]:checked');
    return selected ? selected.value : 'only-changes'; // fallback para only-changes
  }


  function renderImagePreviews() {
    const container = document.getElementById('image-previews');
    container.innerHTML = '';
  
    const total = window.selectedImages.length;
    if (total > 7) {
      const wrapper = document.createElement('div');
      wrapper.className = 'file-icon flex items-center space-x-2 text-gray-700';
  
      wrapper.innerHTML = `
        <i class="fas fa-images text-blue-500"></i>
        <span>${total} imagens selecionadas</span>
        <span class="remove-all-images text-red-500 cursor-pointer text-lg ml-2">&times;</span>
      `;
      
      container.appendChild(wrapper);
  
      // Handler para remover todas
      wrapper.querySelector('.remove-all-images').addEventListener('click', () => {
        window.selectedImages = [];
        renderImagePreviews();
      });
      return;
    }
  
    window.selectedImages.forEach((file, index) => {
      const reader = new FileReader();
      reader.onload = function (e) {
        const wrapper = document.createElement('div');
        wrapper.className = 'relative';
  
        wrapper.innerHTML = `
          <img src="${e.target.result}" alt="preview" class="w-16 h-16 object-cover rounded border border-gray-500 shadow">
          <span class="remove-image absolute top-[-6px] right-[-6px] bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center cursor-pointer" data-index="${index}">&times;</span>
        `;
        container.appendChild(wrapper);
      };
      reader.readAsDataURL(file);
    });
  }
    
  function renderAttachedFiles() {
    console.log("🔁 Chamando renderAttachedFiles()");
    attachedFiles.innerHTML = '';

    const total = window.selectedFiles.length;
    if (total > 7) {
      const wrapper = document.createElement('div');
      wrapper.className = 'file-icon flex items-center space-x-2 text-gray-700';

      wrapper.innerHTML = `
        <i class="fas fa-file-alt text-blue-500"></i>
        <span>${total} selected files</span>
        <span class="remove-all-files text-red-500 cursor-pointer text-lg ml-2">&times;</span>
      `;
      
      attachedFiles.appendChild(wrapper);

      // Handler para remover todos
      wrapper.querySelector('.remove-all-files').addEventListener('click', () => {
        window.selectedFiles = [];
        renderAttachedFiles();
      });
      return;
    }

    (window.selectedFiles || []).forEach((file, index) => {
      const fileEl = document.createElement('div');
      fileEl.className = 'file-icon';
      fileEl.innerHTML = `
        <i class="fas fa-file-alt"></i> ${file.name}
        <span class="remove-file" data-index="${index}">&times;</span>
      `;
      attachedFiles.appendChild(fileEl);
    });
  }


  // 💬 Enviar mensagem
  sendButton.addEventListener('click', () => {
    const messageText = messageInput.value;
    generateResponse(messageText);
  
    // Limpar campos
    messageInput.value = '';
    window.selectedFiles = [];
    window.selectedImages = [];
    renderAttachedFiles();
    renderImagePreviews();
  });
  
  messageInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      const messageText = messageInput.value;
  
      generateResponse(messageText);
  
      // Limpar campos
      messageInput.value = '';
      window.selectedFiles = [];
      window.selectedImages = [];
      renderAttachedFiles();
      renderImagePreviews();
    }
  });
  

  // ⚙️ Configurações
  settingsButton.addEventListener('click', function () {
    settingsModal.classList.remove('hidden');
  });
  settingsButton2.addEventListener('click', function () {
    settingsModal.classList.remove('hidden');
  });

  closeSettings.addEventListener('click', function () {
    settingsModal.classList.add('hidden');
  });

  window.addEventListener('click', function (event) {
    if (event.target === settingsModal) {
      settingsModal.classList.add('hidden');
    }
  });

  // Novo chat
  newChatButton.addEventListener('click', async () => {
    clearChat();
    await NewChat();
    
  });

  // connectfirebase.addEventListener('click', function () {
  //   clearChat();
  // });

  console.log("📦 Elemento attached-files:", document.getElementById('attached-files'));
  
  window.getSCIAMode = getSCIAMode;
  window.renderImagePreviews = renderImagePreviews;
  window.renderAttachedFiles = renderAttachedFiles;
  window.selectedFiles = selectedFiles;
  
  // Você pode ativar depois se quiser carregar as conversas automaticamente:
  // loadConversation();
}

  
console.log("🔥 Chat carregado!");

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 DOM completamente carregado!");
  checkSessionThenInit();
  loadSettings();
  
  iniciarContadorDeAgentes();
  atualizarContadorRepos();
  loadStatus();
  initWebSocket();
  initChatUI();
  // setInterval(() => {
  //   loadConversation(localStorage.getItem('session_id'));
  // }, 60000);
  loadAllChats();
  checkDBConnectionStatus();
  setInterval(() => {
    checkDBConnectionStatus();
  }, 90000);
  

  loadAPIandLimits()
  const toggleBtn = document.getElementById("toggle-editor");
  if (toggleBtn) toggleBtn.click();

});
