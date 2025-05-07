// JavaScript for the Agent Detail page

document.addEventListener('DOMContentLoaded', async function() {
  // Set current year in footer
  document.getElementById('current-year').textContent = new Date().getFullYear();
  
  // Get agent ID from URL
  const urlParams = new URLSearchParams(window.location.search);
  const agentId = urlParams.get('id');
  
  if (!agentId) {

      console.log('Settings :', agentId);
      // redirectToNotFound();
      return;
  }
  
  // Inicializa a página com os dados do agente
  await initializeAgentPage(agentId);
  
  // Set up back button
  document.getElementById('back-button').addEventListener('click', function() {
      window.location.href = 'index.html';
  });

  // Set up settings form
  setupSettingsForm();
});


function setupSettingsForm() {
  const settingsButton = document.getElementById('settings-button');
  const settingsModal = document.getElementById('settings-modal');
  const closeSettings = document.getElementById('close-settings');
  const saveSettingsButton = document.querySelector('#settings-modal button:last-of-type');
  
  // Open settings modal
  settingsButton.addEventListener('click', function() {
    // Load saved settings before showing the modal
    loadSettings();
    settingsModal.classList.remove('hidden');
  });
  
  // Close settings modal
  closeSettings.addEventListener('click', function() {
    settingsModal.classList.add('hidden');
  });
  
  // Close modal when clicking outside
  window.addEventListener('click', function(event) {
    if (event.target === settingsModal) {
      settingsModal.classList.add('hidden');
    }
  });
  
  // Save settings when form is submitted
  saveSettingsButton.addEventListener('click', function() {
    saveSettings();
    settingsModal.classList.add('hidden');
    
    // Show success toast/notification
    showNotification('Settings saved successfully');
  });
}

// Set up tabs functionality
function setupTabs() {
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabPanes = document.querySelectorAll('.tab-pane');
  
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      // Remove active class from all buttons and panes
      tabButtons.forEach(btn => {
        btn.classList.remove('active');
        btn.classList.remove('text-blue-600');
        btn.classList.remove('border-blue-600');
        btn.classList.add('border-transparent');
      });
      
      tabPanes.forEach(pane => {
        pane.classList.remove('active');
        pane.classList.add('hidden');
      });
      
      // Add active class to clicked button
      button.classList.add('active');
      button.classList.add('text-blue-600');
      button.classList.add('border-blue-600');
      button.classList.remove('border-transparent');
      
      // Show corresponding tab pane
      const tabId = button.getAttribute('data-tab');
      const tabPane = document.getElementById(tabId);
      if (tabPane) {
        tabPane.classList.add('active');
        tabPane.classList.remove('hidden');
      }
    });
  });
  
  // Set active tab based on URL hash, or default to overview
  const hash = window.location.hash.substring(1);
  if (hash && document.getElementById(hash)) {
    document.querySelector(`[data-tab="${hash}"]`)?.click();
  } else {
    // Default tab is already set in HTML
  }
  
  // Update hash when changing tabs
  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const tabId = button.getAttribute('data-tab');
      window.location.hash = tabId;
    });
  });
}

// Carrega as configurações utilizando os dados do agente
function loadSettings(agent) {
  const apiKeyInput = document.getElementById('api-key');
  const keyAgentInput = document.getElementById('key-agent');
  const githubCompanyInput = document.getElementById('github-company');
  const githubTypeSelect = document.getElementById('github-type-project');
  const modelSelect = document.getElementById('model-agent');
  
  // Preencher os campos com os valores do agente
  apiKeyInput.value = agent.apikey || '';
  keyAgentInput.value = agent.agent_key || '';
  githubCompanyInput.value = agent.companyname || '';
  githubTypeSelect.value = agent.private_project ? 'True' : 'False';
  modelSelect.value = agent.modelSelect || 'default';
}

// Save settings to localStorage
function saveSettings() {
  const apiKeyInput = document.getElementById('api-key');
  const keyAgentInput = document.getElementById('key-agent');
  const githubCompanyInput = document.getElementById('github-company');
  const githubTypeSelect = document.getElementById('github-type-project');
  const modelSelect = document.getElementById('model-agent');
  const workModeSelect = document.querySelector('#settings-modal select:last-of-type');
  const developmentModeCheckboxes = document.querySelectorAll('#settings-modal input[type="checkbox"]');
  
  // Get current agent ID
  const urlParams = new URLSearchParams(window.location.search);
  const agentId = urlParams.get('id');
  
  // Collect development modes
  const developmentModes = [];
  developmentModeCheckboxes.forEach(checkbox => {
    if (checkbox.checked) {
      developmentModes.push(checkbox.nextElementSibling.textContent.trim().toLowerCase());
    }
  });
  
  // Create settings object
  const settings = {
    apiKey: apiKeyInput.value,
    keyAgent: keyAgentInput.value,
    companyName: githubCompanyInput.value,
    privateProject: githubTypeSelect.value === 'True',
    model: modelSelect.value,
    workMode: workModeSelect.value,
    developmentModes: developmentModes
  };
  
  // Save settings to localStorage with agent ID as part of the key
  localStorage.setItem(`agent_settings_${agentId}`, JSON.stringify(settings));
  
  // Also update as current global settings
  localStorage.setItem('current_agent_settings', JSON.stringify(settings));
  
  console.log('Settings saved:', settings);
}

// Função principal para inicializar a página
async function initializeAgentPage(agentId) {
  try {
    // Buscar dados do agente
    const agent = await fetchAgentData(agentId);
    
    if (!agent) {
        console.log('initializeAgentPage:', agent);
        // redirectToNotFound();
        return;
    }
    
    // Armazenar para uso global se necessário
    window.currentAgent = agent;
    
    // Preencher detalhes do agente na interface
    populateAgentDetails(agent);
    
    // Preencher configurações
    loadSettings(agent);
    
    // Configurar abas
    setupTabs();
  } catch (error) {
    console.error('Error initializing agent page:', error);
    displayErrorMessage('Failed to initialize agent page. Please try again later.');
  }
}


// Fetch agent data from API
async function fetchAgentData(agentId) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 195000); // 15 segundos

  try {
    const response = await fetch('https://softwareai-library-hub.rshare.io/api/agents', {
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error('Failed to fetch agents');
    }

    const agents = await response.json();
    return agents.find(a => a.id === agentId) || null;
  } catch (error) {
    console.error('Error fetching agents:', error.name === 'AbortError' ? 'Request timed out' : error);
    displayErrorMessage('Failed to load agent details. Please try again later.');
    return null;
  }
}


// Show notification
function showNotification(message) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-4 py-2 rounded shadow-lg transition-opacity duration-300';
  notification.textContent = message;
  
  // Add to document
  document.body.appendChild(notification);
  
  // Remove after 3 seconds
  setTimeout(() => {
    notification.style.opacity = '0';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// Load agent details
function loadAgentDetails(agentId) {
  // Find the agent with the matching ID
  const agent = window.agents.find(a => a.id === agentId);

  if (!agent) {
      // redirectToNotFound();
      console.log('loadAgentDetails:', agent);
      return;
  }
  
  // Populate agent details
  loadSettings(agentId);
  
  // Populate agent details
  populateAgentDetails(agent);
  
  // Set up tabs
  setupTabs();
  
}

// Atualiza a função populateAgentDetails para incluir os "Use Cases"
function populateAgentDetails(agent) {
    // Set agent header
    const agentHeader = document.getElementById('agent-header');
    agentHeader.innerHTML = `
      <div class="w-16 h-16 rounded-md bg-blue-100 text-blue-600 flex items-center justify-center">
        <i class="${agent.icon} text-3xl"></i>
      </div>
      <div>
        <h1 class="text-2xl font-bold">${agent.name}</h1>
        <p class="text-gray-600">${agent.shortDescription}</p>
      </div>
    `;

    // Set agent description
    document.getElementById('agent-description').textContent = agent.fullDescription;

    // Render markdown about
    if (agent.about) {
        document.getElementById('markdown-about-content').innerHTML = marked.parse(agent.about);
    }
    // Render markdown about
    if (agent.tutorial) {
      document.getElementById('markdown-tutorial-content').innerHTML = marked.parse(agent.tutorial);
    }
    
    // Render "Use Cases" se existirem
    const useCasesContainer = document.getElementById('agent-use-cases');
    if (agent.UseCases) {
        useCasesContainer.innerHTML = agent.UseCases.split("\n").map(uc => `<li>${uc.trim()}</li>`).join("");
    } else {
        useCasesContainer.innerHTML = "<li class='text-gray-500'>No use cases provided</li>";
    }
    const loader = document.getElementById('agent-config-loader');
    // Esconde o loader após preencher os dados
    if (loader) loader.style.display = 'none';
}

// Set up tabs functionality
function setupTabs() {
  const tabButtons = document.querySelectorAll('.tab-button');
  const tabPanes = document.querySelectorAll('.tab-pane');
  
  tabButtons.forEach(button => {
      button.addEventListener('click', () => {
          // Remove active class from all buttons and panes
          tabButtons.forEach(btn => {
              btn.classList.remove('active');
              btn.classList.remove('text-blue-600');
              btn.classList.remove('border-blue-600');
              btn.classList.add('border-transparent');
          });
          
          tabPanes.forEach(pane => {
              pane.classList.remove('active');
              pane.classList.add('hidden');
          });
          
          // Add active class to clicked button
          button.classList.add('active');
          button.classList.add('text-blue-600');
          button.classList.add('border-blue-600');
          button.classList.remove('border-transparent');
          
          // Show corresponding tab pane
          const tabId = button.getAttribute('data-tab');
          const tabPane = document.getElementById(tabId);
          if (tabPane) {
              tabPane.classList.add('active');
              tabPane.classList.remove('hidden');
          }
      });
  });
}

// Display error message to the user
function displayErrorMessage(message) {
  const container = document.querySelector('main .container');
  if (container) {
      const errorDiv = document.createElement('div');
      errorDiv.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded my-4';
      errorDiv.innerHTML = `<p>${message}</p>`;
      
      const backButton = document.getElementById('back-button');
      container.insertBefore(errorDiv, backButton.nextSibling);
  }
}

// Redirect to 404 page
function redirectToNotFound() {
  window.location.href = '404.html';
}