
function getReposSelecionados(dropdownId) {
  const checkboxes = document.querySelectorAll(`input[name="${dropdownId}-repo"]:checked`);
  const values = Array.from(checkboxes).map(cb => cb.value);
  console.log(`🔍 Repositórios selecionados (${dropdownId}):`, values);
  return values;
}

function getAgentesSelecionados() {
    const checkboxes = document.querySelectorAll('input[name="agent-selection"]:checked');
    return Array.from(checkboxes).map(cb => cb.value);
  }

document.getElementById("save-settings").addEventListener("click", () => {
  const userEmail = localStorage.getItem("userEmail");
  if (!userEmail) {
    alert("Usuário não autenticado.");
    return;
  }

  const agentesSelecionados = getAgentesSelecionados();
  const githubRepositoriesKnowledge = getReposSelecionados("repoDropdownKnowledge");
  const githubRepositoriesWorkspace = getReposSelecionados("repoDropdownWorkspace");
  

  const agentWorkMode = document.querySelector('div[data-content="general"] select')?.value || "";
  const githubTypeProject = document.getElementById("github-type-project")?.value || "";

  const sciaAlgorithm = document.getElementById("SCIA-Selector")?.value || "";
  const sciamode = document.querySelector('input[name="scia-mode"]:checked')?.value || "only-changes";
  const stripeSecretKey = document.getElementById("STRIPE-SECRET-KEY").value;
  const stripePublicKey = document.getElementById("STRIPE-PUBLIC-KEY").value;
  const gmail_usuario = document.getElementById("gmail-usuario").value;
  const gmail_senha = document.getElementById("gmail-senha").value;
  const githubCompany = document.getElementById("owner-repo").value;

  const data = {
    email: userEmail,
    selectedAgents: agentesSelecionados,
    agentWorkMode,
    githubCompany,
    githubRepositoriesKnowledge,
    githubRepositoriesWorkspace,
    githubTypeProject,
    sciamode,
    sciaAlgorithm,
    stripeSecretKey,
    stripePublicKey,
    gmail_usuario,
    gmail_senha,
  };

  console.log("📦 Dados enviados:", data);
  const api_url_save_settings = "https://softwareai.rshare.io/api/save-settings";
  fetch(api_url_save_settings, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(result => {
      alert("Configurações salvas com sucesso!");
    })
    .catch(err => {
      console.error("Erro ao salvar:", err);
      alert("Erro ao salvar configurações.");
    });
});
