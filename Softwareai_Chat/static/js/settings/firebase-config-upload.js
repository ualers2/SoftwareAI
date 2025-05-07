// firebase-config-upload.js
document.getElementById("firebase-config-upload").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const content = await file.text();
  const config = JSON.parse(content);

  // 👉 salvar no escopo global para outro script acessar
  window.firebaseConfig = config;

  alert("Firebase configuration loaded. Now click on 'Connect with Firebase'.");
}
);
