// Carregamento do Monaco Editor
require.config({ paths: { vs: "https://cdn.jsdelivr.net/npm/monaco-editor@0.44.0/min/vs" } });

let editor;
require(["vs/editor/editor.main"], function () {
  editor = monaco.editor.create(document.getElementById("monaco-container"), {
    value: "<!-- Digite seu código HTML aqui -->\n<h1>Hello, Monaco!</h1>",
    language: "html",
    theme: "vs-dark",
    automaticLayout: true,
  });
  window.editor = editor

  // Atualizar preview ao vivo - colocar aqui
  const previewFrame = document.getElementById("preview-frame");
  editor.onDidChangeModelContent(() => {
    const html = editor.getValue();
    previewFrame.srcdoc = html;
  });
});

// Elementos do layout
const editorPanel = document.getElementById("code-editor-panel");
const chatMain = document.getElementById("chat-main");

// Toggle do editor
document.getElementById("toggle-editor").addEventListener("click", () => {
  const isOpen = !editorPanel.classList.contains("w-0");

  if (isOpen) {
    // Fechar
    chatMain.classList.remove("md:w-3/5");
    chatMain.classList.add("w-full");

    editorPanel.classList.remove("md:w-2/5");
    editorPanel.classList.add("w-0", "overflow-hidden");
  } else {
    // Abrir
    chatMain.classList.remove("w-full");
    chatMain.classList.add("md:w-3/5");

    editorPanel.classList.remove("w-0", "overflow-hidden");
    editorPanel.classList.add("md:w-2/5");
  }
});

// Botão de fechar manual
document.getElementById("close-editor").addEventListener("click", () => {
  chatMain.classList.remove("md:w-3/5");
  chatMain.classList.add("w-full");

  editorPanel.classList.remove("md:w-2/5");
  editorPanel.classList.add("w-0", "overflow-hidden");
});
