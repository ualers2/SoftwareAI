async function checkDBConnectionStatus() {
  const userEmail = localStorage.getItem("user_email");
  if (!userEmail) return;

  try {
    const res = await fetch(`https://softwareai.rshare.io/api/check-firebase-config?email=${encodeURIComponent(userEmail)}`);
    const data = await res.json();

    const statusEl = document.getElementById("firebase-connected-status");
    const inputEl = document.getElementById("firebase-config-upload");
    const buttonEl = document.getElementById("connect-firebase");

    if (data.status === "connected") {
      statusEl.textContent = "Connected";
      statusEl.classList.replace("text-yellow-400", "text-green-400");

      // Ocultar input e botão
      if (inputEl) inputEl.classList.add("hidden");
      if (buttonEl) buttonEl.classList.add("hidden");
    } else {
      statusEl.textContent = "Disconnected";
      statusEl.classList.replace("text-green-400", "text-yellow-400");

      // Mostrar input e botão se estavam ocultos
      if (inputEl) inputEl.classList.remove("hidden");
      if (buttonEl) buttonEl.classList.remove("hidden");
    }
  } catch (err) {
    console.error("Erro ao checar status Firebase:", err);
  }
}
