async function loadSettings() {
  const email = localStorage.getItem("userEmail");
  const githubToken = localStorage.getItem("githubToken");

  console.log("🧾 Email localStorage:", email);
  console.log("🧾 GitHub Token localStorage:", githubToken);

  if (!email || !githubToken) {
    console.warn("⚠️ Email ou GitHub Token não encontrados no localStorage. Abortando loadSettings.");
    return;
  }
  try {
    const api_url_load_settings = "https://softwareai.rshare.io/api/load-settings";
    const res = await fetch(api_url_load_settings, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email })
    });

    const data = await res.json();
    console.log("📦 Dados carregados do backend:", data);

    document.getElementById("owner-repo").value = data.githubCompany || "";
    document.getElementById("github-type-project").value = data.githubTypeProject || "False";

    document.getElementById("STRIPE-SECRET-KEY").value = data.stripeSecretKey;
    document.getElementById("STRIPE-PUBLIC-KEY").value = data.stripePublicKey;
    document.getElementById("gmail-usuario").value = data.gmail_usuario;
    document.getElementById("gmail-senha").value = data.gmail_senha;
    

    document.querySelector('select:not(#github-type-project):not(#model-agent)').value = data.agentWorkMode || "conversecompose";
    document.getElementById("SCIA-Selector").value = data.sciaAlgorithm || "SCIA-v1";
    if (data.sciamode) {
      const radio = document.querySelector(`input[name="scia-mode"][value="${data.sciamode}"]`);
      if (radio) {
        radio.checked = true;
      }
    }

    const selected = Array.isArray(data.selectedAgents) ? data.selectedAgents : [];
    const githubRepositoriesKnowledge = Array.isArray(data.githubRepositoriesKnowledge) ? data.githubRepositoriesKnowledge : [];
    const githubRepositoriesWorkspace = Array.isArray(data.githubRepositoriesWorkspace) ? data.githubRepositoriesWorkspace : [];
    
    // if (data.selectedFolderName) {
    //   const folderButton = document.getElementById("folderPicker");
    //   const folderIcon = document.getElementById("folder-icon");
      
    //   folderIcon.classList.remove("fa-folder");
    //   folderIcon.classList.add("fa-folder-open", "text-green-400");
    //   folderButton.title = `Pasta: ${data.selectedFolderName}`;
      
    //   // Salva no localStorage para reaproveitamento
    //   localStorage.setItem("selectedFolderName", data.selectedFolderName);
    // }
    
    await loadAgents(selected); // se loadAgents aceitar parâmetro para selecionar agentes
    await carregarRepositoriosEGithubOrgs(githubToken, githubRepositoriesKnowledge, githubRepositoriesWorkspace);

    iniciarContadorDeAgentes2();

  } catch (err) {
    console.error("Erro ao carregar configurações:", err);
  }
}

async function loadAPIandLimits() {
  const email = localStorage.getItem("userEmail");
  try {
    const api_url_load_settings = "https://softwareai.rshare.io/api/load-apikey-and-limits";
    const res = await fetch(api_url_load_settings, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email })
    });

    const data = await res.json();
    console.log("📦 Dados  load-apikey-and-limits carregados do backend:", data);

    document.getElementById("api-token").innerText = `Api Token: ${data.api_key}` || "API TOKEN: None";
    document.getElementById("my-limits-message").innerText = `Message Limits: ${data.limit}` || "";
    

  } catch (err) {
    console.error("Erro ao carregar configurações:", err);
  }

}
