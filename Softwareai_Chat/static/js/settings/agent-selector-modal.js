
const agentSelectorModal = document.getElementById("agent-selector-modal-chat");
const openAgentSelectorBtn = document.getElementById("open-agent-selector");
const closeAgentSelectorBtn = document.getElementById("close-agent-selector");

openAgentSelectorBtn.addEventListener("click", () => {
    agentSelectorModal.classList.remove("hidden");
});

closeAgentSelectorBtn.addEventListener("click", () => {
    agentSelectorModal.classList.add("hidden");
});

// Fecha o modal se clicar fora
document.addEventListener("click", (e) => {
    if (!agentSelectorModal.contains(e.target) && !openAgentSelectorBtn.contains(e.target)) {
        agentSelectorModal.classList.add("hidden");
    }
});

