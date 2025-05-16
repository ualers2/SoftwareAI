document.getElementById("reset-settings").addEventListener("click", () => {
    if (!confirm("Tem certeza que deseja resetar as configurações para os valores padrão?")) return;
  
    document.getElementById("key-agent").value = "";
    document.getElementById("github-company").value = "";
    document.getElementById("github-type-project").value = "False";
    document.getElementById("model-agent").value = "gpt-4o-mini-2024-07-18";

    document.querySelector('select:not(#github-type-project):not(#model-agent)').value = "conversecompose";
  
    document.querySelectorAll('input[type="checkbox"]').forEach(cb => {
      cb.checked = false;
    });
  
    alert("Configurações resetadas.");
  });
  