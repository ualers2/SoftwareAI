async function checkStripeConnectionStatus() {
    const email = localStorage.getItem("userEmail");
    if (!email) {
      console.warn("⚠️ Email do usuário não encontrado no localStorage.");
      return;
    }
  
    try {
      const res = await fetch("https://softwareai.rshare.io/api/stripe-connection-status", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ email })
      });
  
      const data = await res.json();
  
      const statusEl = document.getElementById("stripe-connected-status");
  
      if (!statusEl) return;
  
      if (data.connected) {
        statusEl.textContent = "Conectado";
        statusEl.classList.remove("text-yellow-400");
        statusEl.classList.add("text-green-400");
      } else {
        statusEl.textContent = "Desconectado";
        statusEl.classList.remove("text-green-400");
        statusEl.classList.add("text-yellow-400");
      }
    } catch (err) {
      console.error("Erro ao verificar conexão com Stripe:", err);
    }
}
  