document.getElementById("reset-firebase").addEventListener("click", async () => {
    const userEmail = localStorage.getItem("user_email");
    if (!userEmail) {
      alert("Sessão expirada. Faça login novamente.");
      return window.location.href = "/login";
    }
  
    const confirmReset = confirm("Tem certeza que deseja resetar suas configurações do Firebase?");
    if (!confirmReset) return;
  
    try {
      const res = await fetch("https://softwareai.rshare.io/api/reset-firebase-config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: userEmail }),
      });
  
      if (res.ok) {
        alert("Configurações Firebase resetadas com sucesso!");
  
        // Atualiza status e reexibe input e botão de conexão
        document.getElementById("firebase-connected-status").textContent = "Disconnected";
        document.getElementById("firebase-connected-status").classList.replace("text-green-400", "text-yellow-400");
  
        document.getElementById("firebase-config-upload").classList.remove("hidden");
        document.getElementById("connect-firebase").classList.remove("hidden");
      } else {
        alert("Erro ao resetar configuração.");
      }
    } catch (err) {
      console.error("Erro ao resetar Firebase:", err);
      alert("Erro ao resetar configuração.");
    }
  });
  