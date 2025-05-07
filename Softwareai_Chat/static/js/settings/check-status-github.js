function loadStatus() {
  const api_url_github_status = "https://softwareai.rshare.io/api/github/status";
  fetch(api_url_github_status, {
    credentials: 'include'
  })
    .then(res => res.json())
    .then(data => {
      const btnEl = document.getElementById("github-btn");

      if (!btnEl) return;

      if (data.connected) {
        btnEl.classList.add("connected");
        btnEl.innerHTML = `<i class="fab fa-github"></i><span>Connected</span>`;
        btnEl.onclick = null; // desativa o clique se estiver conectado
        carregarRepositoriosEGithubOrgs(data.access_token, data.githubRepositories);
        console.log("📤 Repositórios que serão enviados para marcar os checkboxes:", data.githubRepositories);
      } else {
        btnEl.classList.remove("connected");
        btnEl.innerHTML = `<i class="fab fa-github"></i><span>Connect with GitHub</span>`;
        btnEl.onclick = () => {
          window.location.href = "https://softwareai.rshare.io/login/github";
        };
      }

    })
    .catch(err => console.error("Erro ao verificar status GitHub:", err));
}
