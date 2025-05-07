console.log("🔥 tool_detail carregado!");
function extrairFuncoes(codigo) {
    const linhas = codigo.split('\n');
    const blocos = [];
    let capturando = false;
    let capturandoTipo = false;
    let blocoAtual = [];
    let indentacaoBase = null;

    for (let i = 0; i < linhas.length; i++) {
        const linha = linhas[i].trimEnd();

        // Detecta decorator @function_tool
        if (linha.trim().startsWith('@function_tool')) {
            capturando = true;
            blocoAtual = [linha];
            continue;
        }

        // Captura classe TypedDict
        if (linha.match(/^class\s+\w+\s*\(\s*TypedDict\s*\)\s*:/)) {
            capturandoTipo = true;
            blocoAtual = [linha];
            const matchIndent = linha.match(/^(\s*)class /);
            indentacaoBase = matchIndent ? matchIndent[1] : '';
            i++;

            while (i < linhas.length) {
                const linhaAtual = linhas[i];
                if (linhaAtual.startsWith(indentacaoBase + ' ') || linhaAtual.startsWith(indentacaoBase + '\t')) {
                    blocoAtual.push(linhas[i]);
                    i++;
                } else {
                    break;
                }
            }

            blocos.push(blocoAtual.join('\n'));
            capturandoTipo = false;
            indentacaoBase = null;
            i--; // Corrige avanço extra
            continue;
        }

        // Captura função decorada
        if (capturando && linha.trim().startsWith('def ')) {
            blocoAtual.push(linha);
            const matchIndent = linha.match(/^(\s*)def /);
            indentacaoBase = matchIndent ? matchIndent[1] : '';
            i++;

            while (i < linhas.length) {
                const linhaAtual = linhas[i];
                if (linhaAtual.startsWith(indentacaoBase + ' ') || linhaAtual.startsWith(indentacaoBase + '\t')) {
                    blocoAtual.push(linhaAtual);
                    i++;
                } else {
                    break;
                }
            }

            blocos.push(blocoAtual.join('\n'));
            capturando = false;
            indentacaoBase = null;
            i--; // Corrige avanço extra
        }
    }

    return blocos.join('\n\n');
}


document.addEventListener("DOMContentLoaded", async function() {
    console.log("🚀 DOM completamente carregado!");

    const toolId = typeof TOOL_ID !== "undefined" ? TOOL_ID : null;
    console.log("toolId =", toolId);
    const response = await fetch("https://softwareai-library-hub.rshare.io/api/list-tools");
    const allTools = await response.json();
    const tool = allTools.find(t => t.id === toolId);
    console.log(`tool ${tool}`);

    if (tool) {
        document.getElementById("tool-name").textContent = tool.id;
        document.getElementById("tool-description").textContent = `Purpose of the tool: ${tool.fullDescription}`;

        // Carregar metadata antes do clique
        const metaResp = await fetch(`https://softwareai-library-hub.rshare.io/api/tool-metadata/${toolId}`);
        const metadata = await metaResp.json();
        console.info(metadata);
        console.info(metadata.code);
        // Exibir os parâmetros abaixo da descrição
        const params = metadata.function?.parameters?.properties || {};
        const totalParams = Object.keys(params).length;
        document.getElementById("tool-count-properties").textContent = `The tool has ${totalParams} properties`;
        const container = document.getElementById("parameters-container");
        container.innerHTML = ""; // limpa se clicado mais de uma vez

        for (const [key, value] of Object.entries(params)) {
            const paramDiv = document.createElement("div");
            paramDiv.className = "bg-white p-4 rounded shadow";

            paramDiv.innerHTML = `
                <div class="font-semibold text-blue-700">Property: ${key}</div>
                <div class="text-gray-700 text-sm mb-1">Description: ${value.description}</div>
                <div class="text-xs text-gray-500 italic">Type: ${value.type}</div>
            `;

            container.appendChild(paramDiv);
        }

        // Aguardar o botão ser clicado para exibir o conteúdo
        document.getElementById("show-metadata-btn").addEventListener("click", () => {
            // Checar se o modal e o código já estão prontos
            const metadataContent = document.getElementById("metadata-content");
            const codeContent = document.getElementById("code-content");
           
            // Exibir metadata
            if (metadataContent) {
                const originalParams = tool.parameters || {};  // Acessa diretamente as propriedades de 'tool'

                // Garantir que o dicionário 'parameters' tem os campos corretos
                const formattedParams = {
                    type: "object",
                    properties: originalParams.properties || {},  // Acessa diretamente as propriedades
                    required: originalParams.required || []  // Acessa diretamente o campo 'required'
                };

                const formattedMetadata = {
                    type: "function",  // Adicionado "type": "function"
                    function: {
                        name: tool.id,  // Acessa diretamente o 'id' de 'tool'
                        description: (tool.fullDescription || "").replace("\n", " ").trim(),  // Acessa a descrição diretamente
                        parameters: formattedParams
                    }
                };
                const onlyFunction = formattedMetadata || { message: "Função não encontrada." };
                metadataContent.textContent = JSON.stringify(onlyFunction, null, 2);
                Prism.highlightElement(metadataContent);  // Realça JSON

            } else {
                console.warn("⚠️ Elemento #metadata-content não encontrado!");
            }


            // Exibir código
            if (codeContent) {
                const rawCode = metadata.code || "";
                const codeFiltrado = extrairFuncoes(rawCode);
                codeContent.textContent = codeFiltrado || "# Nenhuma função decorada encontrada.";
                Prism.highlightElement(codeContent);  // Realça Python

            }

            // Mostrar o modal
            document.getElementById("metadata-modal").classList.remove("hidden");
        });

        document.getElementById("close-modal").addEventListener("click", () => {
            document.getElementById("metadata-modal").classList.add("hidden");
        });
        // Fechar modal ao clicar fora da caixa de conteúdo
        document.getElementById("metadata-modal").addEventListener("click", function(event) {
            const modalContent = document.querySelector("#metadata-modal > div");
            if (!modalContent.contains(event.target)) {
                this.classList.add("hidden");
            }
        });
        // Botões de cópia
        document.getElementById("copy-code-btn").addEventListener("click", () => {
            const code = document.getElementById("code-content").textContent;
            navigator.clipboard.writeText(code).then(() => {
                alert("Código Python copiado!");
            }).catch(err => {
                console.error("Erro ao copiar:", err);
            });
        });

        document.getElementById("copy-metadata-btn").addEventListener("click", () => {
            const metadata = document.getElementById("metadata-content").textContent;
            navigator.clipboard.writeText(metadata).then(() => {
                alert("Metadata JSON copiado!");
            }).catch(err => {
                console.error("Erro ao copiar:", err);
            });
        });
    }
});
