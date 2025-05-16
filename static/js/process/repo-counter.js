function atualizarContadorRepos() {
  const selecionados = document.querySelectorAll('input[name="github-repo"]:checked');
  const count = selecionados.length;
  const dropdownButton = document.getElementById("dropdownButton");
  if (dropdownButton) {
    dropdownButton.textContent = `Selected repositories: ${count} (for agent's knowledge)`;
  }
}

document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener("change", (event) => {
    if (event.target && event.target.name === "github-repo") {
      atualizarContadorRepos();
    }
  });

  atualizarContadorRepos();
});
