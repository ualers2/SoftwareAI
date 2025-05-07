document.addEventListener("DOMContentLoaded", () => {
  const dropdownButtons = document.querySelectorAll("[data-dropdown-target]");

  dropdownButtons.forEach(button => {
    const dropdownId = button.getAttribute("data-dropdown-target");
    const dropdown = document.getElementById(dropdownId);

    if (!dropdown) return;

    // Toggle dropdown
    button.addEventListener("click", (event) => {
      event.stopPropagation();
      dropdown.classList.toggle("hidden");
    });

    // Fecha ao clicar fora
    document.addEventListener("click", (event) => {
      if (!dropdown.contains(event.target) && !button.contains(event.target)) {
        dropdown.classList.add("hidden");
      }
    });

    // Atualiza texto quando usuário marcar/desmarcar checkboxes
    dropdown.addEventListener("change", () => {
      atualizarTextoBotao(dropdown, button);
    });
  });
});
