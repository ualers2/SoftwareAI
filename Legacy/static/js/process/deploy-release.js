document.getElementById("deploy-release").addEventListener("click", async () => {
    const repoUrl = prompt("Cole aqui o link do repositório GitHub que deseja deployar:");
    if (!repoUrl) return;
  
    const res = await fetch("https://softwareai.rshare.io/api/release/deploy", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ repo_url: repoUrl })
    });
  
    const data = await res.json();
    if (data.success) {
      alert("Deploy iniciado com sucesso! Link: " + data.url);
      window.open(data.url, "_blank");
    } else {
      alert("Erro no deploy: " + (data.error || "erro desconhecido"));
    }
  });
  