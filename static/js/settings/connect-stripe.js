document.addEventListener("DOMContentLoaded", () => {

  document.getElementById("connect-stripe").addEventListener("click", async () => {
    const email = localStorage.getItem("userEmail");

    if (!email) {
      console.warn("⚠️ Email não encontrado no localStorage.");
      return;
    }

    const res = await fetch("https://softwareai.rshare.io/api/create-stripe-onboarding-link", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ email })
    });

    const data = await res.json();

    if (data.url) {
      window.location.href = data.url; // redireciona para o onboarding da Stripe
    } else {
      console.error("Erro ao obter URL de onboarding:", data.error);
    }
  });

});
