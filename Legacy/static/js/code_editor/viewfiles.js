
async function readDirectoryRecursive(directoryHandle) {
    const structure = {};
  
    for await (const entry of directoryHandle.values()) {
      if (entry.kind === "file") {
        const file = await entry.getFile();
        const content = await file.text();
        structure[entry.name] = content;
      } else if (entry.kind === "directory") {
        structure[entry.name] = await readDirectoryRecursive(entry);
      }
    }
  
    return structure;
  }
  
function createFileTree(container, structure, depth = 0) {
    Object.entries(structure).forEach(([name, content]) => {
      const item = document.createElement("div");
      item.classList.add("pl-" + (depth * 4)); // Tailwind indent fake (ou use classes dinâmicas)
      item.style.paddingLeft = `${depth * 1.2}rem`; // indent manual
      item.classList.add("hover:text-green-400");
  
      const isFolder = typeof content !== "string";
  
      if (isFolder) {
        item.innerHTML = `<span class="folder-label cursor-pointer">📁 ${name}</span>`;
        const sub = document.createElement("div");
        sub.classList.add("ml-1");
        createFileTree(sub, content, depth + 1);
        item.appendChild(sub);
      
        // Clique para colapsar ou expandir
        item.querySelector(".folder-label").addEventListener("click", () => {
          sub.classList.toggle("hidden");
        });
      } else {
        item.innerHTML = `📄 ${name}`;
        item.onclick = () => {
          editor.setValue(content);
          monaco.editor.setModelLanguage(editor.getModel(), name.split(".").pop());
        };
      }
  
      container.appendChild(item);
    });
  }

// Constantes
const resizer = document.getElementById("resizer");
const fileTree = document.getElementById("file-tree");
const monacoContainer = document.getElementById("monaco-container");
const toggleFileTreeButton = document.getElementById("toggle-file-tree");
const togglePreviewButton = document.getElementById("toggle-preview-button");
const editorPreviewContainer = document.getElementById("editor-preview-container");
const previewFrame = document.getElementById("preview-frame");
const horizontalResizer = document.getElementById("horizontal-resizer");

// Eventos de resize vertical
resizer.addEventListener("mousedown", (e) => {
  e.preventDefault();
  document.addEventListener("mousemove", resizeVertical);
  document.addEventListener("mouseup", stopResizeVertical);
});

horizontalResizer.addEventListener("mousedown", (e) => {
  e.preventDefault();
  document.addEventListener("mousemove", resizeHorizontal);
  document.addEventListener("mouseup", stopResizeHorizontal);
});

function resizeVertical(e) {
  const minWidth = 50;
  const maxWidth = window.innerWidth - 50;
  const newWidth = Math.min(Math.max(e.clientX, minWidth), maxWidth);
  fileTree.style.width = `${newWidth}px`;
  editorPreviewContainer.style.width = `calc(100% - ${newWidth + 1}px)`;
}

function stopResizeVertical() {
  document.removeEventListener("mousemove", resizeVertical);
  document.removeEventListener("mouseup", stopResizeVertical);
}

function resizeHorizontal(e) {
  const containerHeight = editorPreviewContainer.offsetHeight;
  const offsetTop = editorPreviewContainer.getBoundingClientRect().top;
  const newEditorHeight = Math.min(Math.max(e.clientY - offsetTop, 50), containerHeight - 50);
  monacoContainer.style.height = `${newEditorHeight}px`;
  previewFrame.style.height = `calc(100% - ${newEditorHeight + 1}px)`;
}

function stopResizeHorizontal() {
  document.removeEventListener("mousemove", resizeHorizontal);
  document.removeEventListener("mouseup", stopResizeHorizontal);
}

// Toggle file-tree
toggleFileTreeButton.addEventListener("click", () => {
  const isHidden = fileTree.classList.contains("hidden");
  if (isHidden) {
    fileTree.classList.remove("hidden");
    resizer.classList.remove("hidden");
    fileTree.style.width = "200px";
    editorPreviewContainer.style.width = "calc(100% - 201px)";
    toggleFileTreeButton.innerHTML = "⏴";
  } else {
    fileTree.classList.add("hidden");
    resizer.classList.add("hidden");
    editorPreviewContainer.style.width = "100%";
    toggleFileTreeButton.innerHTML = "⏵";
  }
});

// Toggle preview
togglePreviewButton.addEventListener("click", () => {
  const isHidden = previewFrame.classList.contains("hidden");
  if (isHidden) {
    previewFrame.classList.remove("hidden");
    horizontalResizer.classList.remove("hidden");
    monacoContainer.style.height = "50%";
    previewFrame.style.height = "50%";
    togglePreviewButton.innerHTML = "🔽";
  } else {
    previewFrame.classList.add("hidden");
    horizontalResizer.classList.add("hidden");
    monacoContainer.style.height = "100%";
    togglePreviewButton.innerHTML = "🔼";
  }
});

