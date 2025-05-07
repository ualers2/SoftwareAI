
const modal = document.getElementById("custom-modal");
const plusBtn = document.getElementById("open-custom-modal");

// Toggle do modal
plusBtn.addEventListener("click", () => {
modal.classList.toggle("hidden");
});

// Fecha o modal se clicar fora
document.addEventListener("click", (e) => {
if (!modal.contains(e.target) && !plusBtn.contains(e.target)) {
    modal.classList.add("hidden");
}
});
