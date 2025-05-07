// Main JavaScript file for the Agent Library Hub

document.addEventListener('DOMContentLoaded', function() {
  // Set current year in footer
  document.getElementById('current-year').textContent = new Date().getFullYear();
  
  // Fetch agents from the API and populate them
  fetchAgents();
});

// Fetch agents from the backend API
async function fetchAgents() {
    try {
      const agentsContainer = document.getElementById('agents-container');
      if (!agentsContainer) return;
  
      // Exibir o loader enquanto os dados estão sendo carregados
      agentsContainer.innerHTML = `
        <div class="flex flex-col items-center justify-center gap-4 py-8">
            <div class="loader"></div>
            <p class="text-gray-500 text-sm text-center max-w-sm">
            Loading agents... This may take up to <strong>1 minute</strong> ⏳
            </p>
        </div>
      `;
        
  
      const response = await fetch('https://softwareai-library-hub.rshare.io/api/agents');
      if (!response.ok) {
        throw new Error('Failed to fetch agents');
      }
      
      const agents = await response.json();
      
      // Armazenar agentes globalmente
      window.agents = agents;
      
      // Popula os agentes após o carregamento
      populateAgents(agents);
      setupAgentFilter();
    } catch (error) {
      console.error('Error fetching agents:', error);
      displayErrorMessage('Failed to load agents. Please try again later.');
    }
}

// Populate agents in the agents container
function populateAgents(agents) {
  const agentsContainer = document.getElementById('agents-container');
  
  if (!agentsContainer) return;
  
  // Clear any existing content
  agentsContainer.innerHTML = '';
  
  if (agents.length === 0) {
      agentsContainer.innerHTML = '<p class="text-gray-500">No agents available</p>';
      return;
  }
  
  agents.forEach(agent => {
      const agentCard = createAgentCard(agent);
      agentsContainer.appendChild(agentCard);
  });
}

// Create an agent card element
function createAgentCard(agent) {
  const card = document.createElement('div');
  card.className = 'bg-white rounded-lg shadow overflow-hidden transition-all hover:shadow-md';
  let planClasses = 'bg-gray-200 text-gray-800';
  if (agent.type_plan === 'free') planClasses = 'bg-green-500 text-white';
  if (agent.type_plan === 'premium') planClasses = 'bg-blue-500 text-white';

  card.innerHTML = `
      <div class="p-4 bg-gray-50">
          <div class="flex items-center gap-3">
              <div class="rounded-md bg-white p-2 shadow-sm text-blue-600">
                  <i class="${agent.icon} text-xl"></i>
              </div>
              <h3 class="text-lg font-semibold">${agent.name}</h3>
              <span class="text-xs ${planClasses} px-2 py-0.5 rounded-full">
                ${agent.type_plan}
              </span>
          </div>
      </div>
      <div class="p-4">
          <p class="text-gray-600">${agent.shortDescription}</p>
      </div>
      <div class="p-4 pt-0 flex justify-end">
          <a href="agent.html?id=${agent.id}" class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
              View Agent
          </a>
      </div>
  `;
  
  return card;
}
function setupAgentFilter() {
  const filterSelect = document.getElementById('filter-select');
  const searchInput = document.getElementById('search-input');
  if (!filterSelect || !searchInput || !window.agents) return;

  const agents = window.agents;

  // Contar tipos
  const count = {
    all: agents.length,
    free: agents.filter(a => a.type_plan === 'free').length,
    premium: agents.filter(a => a.type_plan === 'premium').length,
  };

  // Preencher options
  filterSelect.innerHTML = `
    <option value="all">All (${count.all})</option>
    <option value="free">Free (${count.free})</option>
    <option value="premium">Premium (${count.premium})</option>
  `;

  // Função de filtro combinada
  function applyFilters() {
    const selectedPlan = filterSelect.value;
    const searchQuery = searchInput.value.toLowerCase();

    let filteredAgents = window.agents;

    if (selectedPlan !== 'all') {
      filteredAgents = filteredAgents.filter(agent => agent.type_plan === selectedPlan);
    }

    if (searchQuery.trim() !== '') {
      filteredAgents = filteredAgents.filter(agent =>
        agent.name.toLowerCase().includes(searchQuery)
      );
    }

    populateAgents(filteredAgents);
  }

  filterSelect.addEventListener('change', applyFilters);
  searchInput.addEventListener('input', applyFilters);
}


// Display error message to the user
function displayErrorMessage(message) {
  const agentsContainer = document.getElementById('agents-container');
  if (agentsContainer) {
      agentsContainer.innerHTML = `
          <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              <p>${message}</p>
          </div>
      `;
  }
}