// Caches persistentes de seleção
let cachedKnowledgeRepos = [];
let cachedWorkspaceRepos = [];

async function carregarRepositoriosEGithubOrgs(token, selectedKnowledgeRepos = [], selectedWorkspaceRepos = []) {
  const headers = {
    Authorization: `Bearer ${token}`,
    Accept: 'application/vnd.github+json'
  };

  try {
    // Buscar organizações onde o usuário é admin
    const orgsResp = await fetch("https://api.github.com/user/memberships/orgs", { headers });
    const orgMemberships = await orgsResp.json();

    console.log("Organizações :", orgMemberships);

    const adminOrgs = orgMemberships
      .filter(m => m.role === "admin" || m.role === "member")
      .map(m => m.organization);
  

    console.log("Organizações (admin):", adminOrgs);

    const orgSelect = document.getElementById('github-company');
    orgSelect.innerHTML = '';
    adminOrgs.forEach(org => {
      const opt = document.createElement('option');
      opt.value = org.login;
      opt.textContent = org.login;
      orgSelect.appendChild(opt);
    });

    // Buscar repositórios do usuário
    const reposResp = await fetch("https://api.github.com/user/repos?per_page=100", { headers });
    const repos = await reposResp.json();

    console.log("Projects :", repos);

    // Preencher os dois dropdowns com checkboxes
    popularRepositoriosComCheckbox(repos, selectedKnowledgeRepos, 'repoDropdownKnowledge');
    popularRepositoriosComCheckbox(repos, selectedWorkspaceRepos, 'repoDropdownWorkspace');

  } catch (err) {
    console.error("Erro ao buscar dados do GitHub:", err);
  }
}


function popularRepositoriosComCheckbox(repos, selectedRepos, dropdownId) {
  selectedRepos = Array.isArray(selectedRepos) ? selectedRepos : [];

  // Determina cache correto com base no dropdownId
  let cachedRepos;
  if (dropdownId === 'repoDropdownKnowledge') {
    if (selectedRepos.length) cachedKnowledgeRepos = selectedRepos;
    cachedRepos = cachedKnowledgeRepos;
  } else if (dropdownId === 'repoDropdownWorkspace') {
    if (selectedRepos.length) cachedWorkspaceRepos = selectedRepos;
    cachedRepos = cachedWorkspaceRepos;
  } else {
    cachedRepos = selectedRepos;
  }

  const normalizedSelected = cachedRepos
    .filter(r => typeof r === 'string')
    .map(r => r.trim().toLowerCase());

  const dropdown = document.getElementById(dropdownId);
  dropdown.innerHTML = "";

  repos.forEach(repo => {
    const item = document.createElement("div");
    item.className = "flex items-center px-4 py-2 hover:bg-gray-800 cursor-pointer";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = repo.full_name;
    checkbox.className = "form-checkbox text-green-500 bg-gray-700 rounded mr-2";
    checkbox.name = dropdownId + "-repo";

    if (normalizedSelected.includes(repo.full_name.toLowerCase())) {
      checkbox.checked = true;
    }

    // Atualiza o cache ao alterar seleção
    checkbox.addEventListener("change", () => {
      const isChecked = checkbox.checked;
      if (dropdownId === 'repoDropdownKnowledge') {
        if (isChecked && !cachedKnowledgeRepos.includes(repo.full_name)) {
          cachedKnowledgeRepos.push(repo.full_name);
        } else if (!isChecked) {
          cachedKnowledgeRepos = cachedKnowledgeRepos.filter(r => r !== repo.full_name);
        }
        localStorage.setItem('cachedKnowledgeRepos', JSON.stringify(cachedKnowledgeRepos));
      } else if (dropdownId === 'repoDropdownWorkspace') {
        if (isChecked && !cachedWorkspaceRepos.includes(repo.full_name)) {
          cachedWorkspaceRepos.push(repo.full_name);
        } else if (!isChecked) {
          cachedWorkspaceRepos = cachedWorkspaceRepos.filter(r => r !== repo.full_name);
        }
        localStorage.setItem('cachedWorkspaceRepos', JSON.stringify(cachedWorkspaceRepos));
      }
    
      const button = document.querySelector(`[data-dropdown-target="${dropdown.id}"]`);
      if (button) atualizarTextoBotao(dropdown, button);
    });
    

    const label = document.createElement("label");
    label.textContent = repo.full_name;
    label.className = "text-sm";

    item.appendChild(checkbox);
    item.appendChild(label);
    dropdown.appendChild(item);
  });

  const button = document.querySelector(`[data-dropdown-target="${dropdown.id}"]`);
  if (button) {
    atualizarTextoBotao(dropdown, button);
  }

  console.log(`✅ [${dropdownId}] Repositórios carregados e marcados.`);
}

// Função reutilizável
function atualizarTextoBotao(dropdown, button) {
  const checkboxes = dropdown.querySelectorAll('input[type="checkbox"]:checked');
  const count = checkboxes.length;

  if (count === 0) {
    button.textContent = "Select repositories...";
  } else if (count === 1) {
    button.textContent = checkboxes[0].value;
  } else {
    button.textContent = `${count} selected repositories`;
  }
}
