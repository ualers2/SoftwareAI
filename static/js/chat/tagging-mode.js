const textarea = document.getElementById('message-input');
const agentModal = document.getElementById('agent-selector-modal-tagging');
const agentList = document.getElementById('agent-list-tagging');
const closeAgentSelector = document.getElementById('close-agent-selector-tagging');

let atIndex = -1;

const storedAgents = localStorage.getItem("agent_names");
const agents = storedAgents ? JSON.parse(storedAgents) : [];

function showAgentModal() {
  agentList.innerHTML = ''; // limpa lista
  agents.forEach(agent => {
    const li = document.createElement('li');
    li.className = 'cursor-pointer hover:bg-gray-700 p-2 rounded flex items-center space-x-2';
    li.innerHTML = `<i class="fas fa-robot text-blue-400"></i> <span>${agent}</span>`;
    li.addEventListener('click', () => selectAgent(agent));
    agentList.appendChild(li);
  });
  agentModal.classList.remove('hidden');
}

closeAgentSelector.addEventListener('click', () => {
  agentModal.classList.add('hidden');
});

function selectAgent(agentName) {
  const text = textarea.value;
  if (atIndex !== -1) {
    const before = text.substring(0, atIndex);
    const after = text.substring(atIndex + 1); // remove o "@"
    textarea.value = `${before}@${agentName} ${after}`;
    textarea.focus();
    textarea.setSelectionRange((before + '@' + agentName + ' ').length, (before + '@' + agentName + ' ').length);
  }
  agentModal.classList.add('hidden');
}

textarea.addEventListener('keyup', (e) => {
  const cursor = textarea.selectionStart;
  const value = textarea.value;

  if (value[cursor - 1] === '@') {
    atIndex = cursor - 1;
    showAgentModal();
  }

  if (!value.includes('@')) {
    atIndex = -1;
    agentModal.classList.add('hidden');
  }
});
