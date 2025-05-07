/**
 * observer-writing.js
 * Observa eventos de digitação e verifica arquivos novos ou modificados na pasta.
 */
/**
 * Retorna uma lista de arquivos que foram adicionados ou modificados desde a última verificação,
 * incluindo arquivos dentro de subpastas, e filtrando por extensão permitida.
 *
 * @param {FileSystemDirectoryHandle} directoryHandle - O handle do diretório selecionado.
 * @param {string} pathPrefix - Prefixo do caminho (usado para subdiretórios).
 * @returns {Promise<File[]>} Array com os arquivos novos ou modificados.
 */

async function getNewOrModifiedFilesFromDirectory(directoryHandle, pathPrefix = '') {
    const newOrModifiedFiles = [];
    const allowedExtensions = ['.js', '.py', '.html', '.css'];
  
    if (!window.folderFileCache) {
      window.folderFileCache = {};
    }
  
    for await (const [name, handle] of directoryHandle.entries()) {
      const fullPath = `${pathPrefix}${name}`;
  
      if (handle.kind === 'file') {
        const ext = name.slice(name.lastIndexOf('.')).toLowerCase();
        if (!allowedExtensions.includes(ext)) continue; // Ignora extensões não permitidas
  
        const file = await handle.getFile();
        const lastModifiedCached = window.folderFileCache[fullPath];
  
        if (!lastModifiedCached || file.lastModified > lastModifiedCached) {
          newOrModifiedFiles.push(file);
          window.folderFileCache[fullPath] = file.lastModified;
        }
      }
  
      if (handle.kind === 'directory') {
        const nestedFiles = await getNewOrModifiedFilesFromDirectory(handle, `${pathPrefix}${name}/`);
        newOrModifiedFiles.push(...nestedFiles);
      }
    }
  
    return newOrModifiedFiles;
}

async function checkForNewOrModifiedFiles() {
  console.log("✅ renderAttachedFiles disponível?", typeof window.renderAttachedFiles);
 
  if (!window.directoryHandle) {
    console.log('Nenhuma pasta selecionada. window.directoryHandle não está definido.');
    return;
  }

  console.log('Verificando arquivos na pasta:', window.directoryHandle.name);

  const mode = getSCIAMode(); // 🔥 define se é all-files ou only-changes
  let files = [];

  try {
    if (mode === 'all-files') {
      console.log('🔄 Modo: ALL-FILES');
      files = await getAllFilesFromDirectory(window.directoryHandle);
    } else {
      console.log('🔍 Modo: ONLY-CHANGES');
      files = await getNewOrModifiedFilesFromDirectory(window.directoryHandle);
    }

    console.log('Arquivos retornados pela verificação:', files);

    const uniqueFiles = files.filter(file => {
      return !window.selectedFiles.some(existingFile => {
        return existingFile.name === file.name && existingFile.lastModified === file.lastModified;
      });
    });

    if (uniqueFiles.length) {
      window.selectedFiles.push(...uniqueFiles);
      showNotification(`${uniqueFiles.length} arquivo(s) detectado(s) para upload.`);

      setTimeout(() => {
        if (typeof renderAttachedFiles === 'function') {
          renderAttachedFiles();
        }
      }, 100);
      console.log(`${uniqueFiles.length} arquivo(s) anexado(s).`);
    } else {
      console.log("Nenhum arquivo novo ou modificado precisa ir pro upload.");
    }

  } catch (error) {
    console.error('Erro ao verificar arquivos na pasta:', error);
  }
}


// Função para exibir notificação discreta
function showNotification(message) {
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.innerText = message;
  document.body.appendChild(notification);
  
  setTimeout(() => {
      notification.remove();
  }, 3000); // A notificação desaparecerá após 3 segundos
}

// Estilos CSS simples para a notificação
const style = document.createElement('style');
style.innerHTML = `
.notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #4CAF50;
  color: white;
  padding: 16px;
  border-radius: 5px;
  z-index: 1000;
  transition: opacity 0.5s ease-in-out;
}
`;
document.head.appendChild(style);

function debounce(func, delay) {
    let timer;
    return function(...args) {
        if (timer) clearTimeout(timer);
        timer = setTimeout(() => {
        func.apply(this, args);
        }, delay);
    };
}

async function getAllFilesFromDirectory(directoryHandle, pathPrefix = '') {
  const allFiles = [];
  const allowedExtensions = ['.js', '.py', '.html', '.css'];

  for await (const [name, handle] of directoryHandle.entries()) {
    const fullPath = `${pathPrefix}${name}`;
    if (handle.kind === 'file') {
      const ext = name.slice(name.lastIndexOf('.')).toLowerCase();
      if (!allowedExtensions.includes(ext)) continue;

      const file = await handle.getFile();
      allFiles.push(file);
    }

    if (handle.kind === 'directory') {
      const nestedFiles = await getAllFilesFromDirectory(handle, `${pathPrefix}${name}/`);
      allFiles.push(...nestedFiles);
    }
  }

  return allFiles;
}

document.addEventListener("DOMContentLoaded", () => {
const messageInput = document.getElementById('message-input');
    if (messageInput) {
        messageInput.addEventListener('input', debounce(() => {
        console.log('Evento de input disparado.');
        checkForNewOrModifiedFiles();
        }, 500)); // 0.5 segundo de debounce
    } else {
        console.warn('Elemento message-input não encontrado.');
    }
});
