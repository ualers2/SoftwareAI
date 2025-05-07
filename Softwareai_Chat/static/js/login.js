const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const msg = document.getElementById('msg');

function showMessage(text, color = "red") {
  msg.textContent = text;
  msg.className = `text-sm text-center text-${color}-400`;
}
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById('login-btn').addEventListener('click', () => {
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const api_url_login = "https://softwareai.rshare.io/api/login";
    fetch(api_url_login, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',  // 👈 necessário para manter a sessã
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      
      showMessage("Login realizado com sucesso!", "green");

      // ✅ Armazena email para uso futuro se quiser
      localStorage.setItem("userEmail", email);
      localStorage.setItem("user_email", email);
      
      // ✅ Redireciona após login, se necessário
      setTimeout(() => {
        window.location.href = "https://softwareai.rshare.io/dashboard";
      }, 1000);
    })
    .catch(err => showMessage("Erro de rede"));
  });

  document.getElementById('register-btn').addEventListener('click', () => {
      const email = emailInput.value.trim();
      const password = passwordInput.value;
      const api_url_register = "https://softwareai.rshare.io/api/register";
      fetch(api_url_register, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
      .then(res => res.json())
      .then(data => {
        if (data.error) return showMessage(data.error);
        
        showMessage("Registro realizado com sucesso!", "green");
    
        // ✅ Armazena email para uso futuro se quiser
        localStorage.setItem("userEmail", email);
        window.location.href = "/dashboard";

      })
      .catch(err => showMessage("Erro de rede"));
  });
});