let cachedSelectedAgents = [];
function slugify(text) {
  return text
    .normalize('NFD')                   // Remove acentos
    .replace(/[\u0300-\u036f]/g, '')    // Remove marcas
    .replace(/[^\w\s-]/g, '')           // Remove símbolos
    .trim()
    .toLowerCase()
    .replace(/[\s_-]+/g, '-');          // Espaços e underlines viram "-"
}

function loadAgents(selectedAgents = []) {
  const loader = document.getElementById("agent-loader");
  const counterText = document.getElementById("agent-counter-text");

  if (selectedAgents.length) {
    cachedSelectedAgents = selectedAgents;
  }
  
  if (loader) loader.style.display = 'flex'; // 👈 mostrar loader
  if (counterText) {
    counterText.textContent = "Loading...";
    counterText.classList.add("animate-pulse", "text-gray-400");
  }
  const api_url_list_agents = "https://softwareai-library-hub.rshare.io/api/agents";

  return fetch(api_url_list_agents)
    .then(res => res.json())
    .then(agents => {
      const agentNames = agents.map(agent => agent.name);
      localStorage.setItem("agent_names", JSON.stringify(agentNames));
      
      const list = document.getElementById("agent-list");
      list.innerHTML = '';
      const listmodal = document.getElementById("agent-list-chat");
      listmodal.innerHTML = '';
    
      const updateCounter = () => {
        const checkboxes = document.querySelectorAll('input[name="agent-selection"]');
        cachedSelectedAgents = Array.from(checkboxes)
          .filter(cb => cb.checked)
          .map(cb => cb.value);

        const count = cachedSelectedAgents.length;
        const counterEl = document.getElementById("agent-counter-text");
        if (counterEl) {
          counterEl.textContent = `${count} agent${count === 1 ? '' : 's'} selected`;
        }
      };

      const selectAllContainer = document.createElement("div");
      selectAllContainer.className = "flex items-center space-x-2 mb-2";
      selectAllContainer.innerHTML = `
        <input type="checkbox" id="select-all-agents" class="form-checkbox h-4 w-4 text-blue-500">
        <label for="select-all-agents" class="text-sm text-gray-300">Select all</label>
      `;
      list.appendChild(selectAllContainer);

      const selectAllCheckbox = selectAllContainer.querySelector("#select-all-agents");

      if (!agents.length) {
        list.innerHTML += '<p class="text-gray-400 text-sm">No agents found.</p>';
        return;
      }

      agents.forEach(agent => {
        const label = document.createElement("label");
        label.className = "flex items-center justify-between space-x-2 p-2 rounded cursor-pointer hover:bg-gray-700 border border-gray-700 transition";
        label.dataset.agentName = agent.name;

        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.name = "agent-selection";
        checkbox.value = agent.name;
        checkbox.className = "form-checkbox h-4 w-4 text-blue-600";

        // ✅ Verifica se está no cache
        if (cachedSelectedAgents.includes(agent.name)) {
          checkbox.checked = true;
        }

        checkbox.addEventListener("change", updateCounter);

        const info = document.createElement("div");
        info.className = "flex items-center space-x-2";

        const dot = document.createElement("span");
        console.info("agent.status:", agent.status);
        dot.className = `h-3 w-3 rounded-full ${agent.status === "running" ? "bg-green-500" : "bg-gray-500"}`;

        const name = document.createElement("span");
        name.textContent = agent.name;
        name.className = "text-white text-sm";

        info.appendChild(dot);
        info.appendChild(name);

        label.appendChild(info);
        label.appendChild(checkbox);
        list.appendChild(label);
        const agentItem = document.createElement("div");
        agentItem.className = "flex items-center justify-between space-x-2 p-2 rounded hover:bg-gray-700 border border-gray-700 transition";
        
        const infomodal = document.createElement("div");
        infomodal.className = "flex items-center space-x-2";
        
        const dotmodal = document.createElement("span");
        dotmodal.className = `h-3 w-3 rounded-full ${agent.status === "running" ? "bg-green-500" : "bg-gray-500"}`;
        
        const namemodal = document.createElement("span");
        
        namemodal.textContent = agent.name;
        namemodal.className = "text-white text-sm";
        
        infomodal.appendChild(dotmodal);
        infomodal.appendChild(namemodal);
        
        const chatBtn = document.createElement("button");
        chatBtn.textContent = "Chat";
        chatBtn.className = "bg-blue-600 px-2 py-1 rounded text-sm hover:bg-blue-500";
        chatBtn.addEventListener("click", async () => {
          const slug = slugify(agent.name);
          localStorage.setItem("active_agent_slug", slug); // <== salvando agente ativo
          window.active_agent_slug = slug;  // Define o agente ativo
          window.active_agent_name = agent.name;  // Define o agente ativo
          clearChat();
          await NewChat();
        });
        
        agentItem.appendChild(infomodal);
        agentItem.appendChild(chatBtn);
        listmodal.appendChild(agentItem);
        
      });

      // Marcar "select all" se todos estiverem marcados
      const allCheckboxes = document.querySelectorAll('input[name="agent-selection"]');
      selectAllCheckbox.checked = allCheckboxes.length > 0 && Array.from(allCheckboxes).every(cb => cb.checked);

      selectAllCheckbox.addEventListener("change", (e) => {
        allCheckboxes.forEach(cb => cb.checked = e.target.checked);
        updateCounter();
      });

      updateCounter();
      if (loader) loader.style.display = 'none'; // 👈 esconder loader

      if (counterText) {
        counterText.classList.remove("animate-pulse", "text-gray-400");
      }
    })
    .catch(err => {
      console.error("Erro ao carregar agentes:", err);
      document.getElementById("agent-list").innerHTML = '<p class="text-red-400 text-sm">Erro ao carregar agentes.</p>';
    });
}
