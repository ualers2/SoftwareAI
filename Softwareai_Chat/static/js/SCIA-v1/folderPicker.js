document.addEventListener("DOMContentLoaded", () => {
  const folderButton = document.getElementById("folderPicker");
  const folderIcon = document.getElementById("folder-icon");

  const lastFolderName = localStorage.getItem("selectedFolderName");
  if (lastFolderName) {
    folderIcon.classList.remove("fa-folder");
    folderIcon.classList.add("fa-folder-open", "text-yellow-400");
    folderButton.title = `Last used folder: ${lastFolderName} (click to reauthorize)`;
    showNotification("Reauthorize access to the folder by clicking the yellow icon.");
  }

  folderButton.addEventListener("click", async () => {
    if (window.showDirectoryPicker) {
      try {
        const directoryHandle = await window.showDirectoryPicker();

        folderIcon.classList.remove("fa-folder", "text-yellow-400");
        folderIcon.classList.add("fa-folder-open", "text-green-400");
        folderButton.title = `Pasta: ${directoryHandle.name}`;
        
        iniciarMonitoramento(directoryHandle);

      } catch (error) {
        console.error('Erro ao selecionar a pasta:', error);
      }
    } else {
      alert('API de seleção de pasta não suportada neste navegador.');
    }
  });
});

async function create_filetree(directoryHandle) {
  const structure = await readDirectoryRecursive(directoryHandle);
  const fileTreeContainer = document.getElementById("file-tree");
  fileTreeContainer.innerHTML = "";
  createFileTree(fileTreeContainer, structure);

}

async function iniciarMonitoramento(directoryHandle) {
  window.directoryHandle = directoryHandle;
  localStorage.setItem("selectedFolderName", directoryHandle.name);

  const opts = { mode: 'readwrite' };
  let perm = await directoryHandle.queryPermission(opts);
  if (perm !== 'granted') {
    perm = await directoryHandle.requestPermission(opts);
  }
  window.directoryWritePermission = (perm === 'granted');

  if (window.directoryWritePermission) {
    showNotification(`SCIA Activated: ${directoryHandle.name} (permissão concedida)`);
    console.log('✅ Permissão de escrita garantida para a pasta:', directoryHandle.name);
  } else {
    showNotification(`SCIA Activated: ${directoryHandle.name} (sem permissão de escrita)`);
    console.warn('⚠️ Permissão de escrita NÃO concedida. Fallback para download padrão.');
  }

  try {
    await create_filetree(window.directoryHandle);
  } catch (error) {
    console.error("Erro inicial ao criar árvore:", error);
  }

  const monitoramentoId = setInterval(async () => {
    try {
      await create_filetree(window.directoryHandle);
    } catch (error) {
      console.error("Erro ao monitorar a pasta:", error);
      if (error.name === "NotFoundError") {
        clearInterval(monitoramentoId);
        showNotification("A pasta foi movida ou excluída. Reautorize o acesso.");

        // Resetar ícone e título
        const folderIcon = document.getElementById("folder-icon");
        const folderButton = document.getElementById("folderPicker");
        folderIcon.classList.remove("fa-folder-open", "text-green-400");
        folderIcon.classList.add("fa-folder", "text-white");
        folderButton.title = "Clique para selecionar uma pasta";

        // Forçar reautorização
        folderButton.classList.add("blink-warning"); // destaque visual
        setTimeout(() => {
          folderButton.classList.remove("blink-warning");
          folderButton.click(); // reautoriza
        }, 3000);
      }
    }
  }, 9000);
}
