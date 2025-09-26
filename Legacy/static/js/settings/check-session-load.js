
function checkSessionThenInit() {
  const api_url_check_session = "https://softwareai.rshare.io/api/check-session";
  fetch(api_url_check_session, { credentials: 'include' })
    .then(res => res.json())
    .then(data => {

      console.log("🧪 Sessão carregada:", data);

      if (data.user) {
        localStorage.setItem("userEmail", data.user);
      }
  
      if (data.githubToken) {
        localStorage.setItem("githubToken", data.githubToken);

      }
      if (data.logged_in) {
        loadAgents(data.selectedAgents || []);
        // iniciarContadorDeAgentes();
        // atualizarContadorRepos();
        // loadStatus();

      } else {
        window.location.href = "https://softwareai.rshare.io/login";  // ou qualquer rota da sua tela de login
      }
    })
    .catch(err => {
      console.error("Erro ao verificar sessão:", err);
      window.location.href = "https://softwareai.rshare.io/login";
    });
}
  