function iniciarContadorDeAgentes() {
  const container = document.getElementById("agent-list");
  const counterText = document.getElementById("agent-counter-text");
  const clearBtn = document.getElementById("clear-agent-selection");

  if (!container || !counterText || !clearBtn) return;

  const atualizarContador = () => {
    const selecionados = container.querySelectorAll("input[type='checkbox']:checked").length;
    counterText.textContent = `${selecionados} agent${selecionados === 1 ? '' : 's'} selected`;
    clearBtn.style.display = selecionados > 0 ? "inline" : "none";
  };

  container.addEventListener("change", atualizarContador);
  atualizarContador(); // inicializa estado

  clearBtn.addEventListener("click", () => {
    container.querySelectorAll("input[type='checkbox']:checked").forEach(input => input.checked = false);
    atualizarContador();
  });

  
}

function iniciarContadorDeAgentes2() {
  const container = document.getElementById("agent-list");
  const counterText = document.getElementById("agent-counter-text");
  const clearBtn = document.getElementById("clear-agent-selection");

  if (!container || !counterText || !clearBtn) return;
  if (counterText) {
    counterText.textContent = "Loading...";
    counterText.classList.add("animate-pulse", "text-gray-400");
  }
  const selecionados = container.querySelectorAll("input[type='checkbox']:checked").length;
  counterText.textContent = `${selecionados} agent${selecionados === 1 ? '' : 's'} selected`;
  clearBtn.style.display = selecionados > 0 ? "inline" : "none";

  clearBtn.onclick = () => {
    container.querySelectorAll("input[type='checkbox']:checked").forEach(input => input.checked = false);
    iniciarContadorDeAgentes2(); // atualiza após limpar
  };

  if (counterText) {
    counterText.classList.remove("animate-pulse", "text-gray-400");
  }
  
}

  