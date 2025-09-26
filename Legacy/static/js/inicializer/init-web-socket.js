// WebSocket connection
let socket;
// Variáveis de controle fora do if para manter estado
let agentWorkflowModal = null;
let agentWorkflowStep = 0;


function initWebSocket() {
    // Connect to the webhook server
    socket = io("https://ace-tahr-41.rshare.io");


    // Listen for webhook data events
    socket.on('webhook_data', async function(data) {
        const payload = data["Chat Agent"];
        
        if (payload?.type === "info") {
            removeTypingIndicator();
            addMessage("agent", payload.message);
        }

        if (payload.type === 'real_stream') {
            removeTypingIndicator();
            handleRealStream(payload);
        } else if (payload.type === 'stream_end') {
            finalizeRealStream();
        }    

        if (payload?.type === "file") {
            let { file_name, file_content_base64 } = payload.message;
            file_name = file_name.replace(/^\/?app\//, '');
            
            const file_extension = file_name.split('.').pop().toLowerCase();
            const isImage = ['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(file_extension);
        
        
            // Se o navegador suportar FileSystemAccess API (somente nos navegadores modernos)
            if ('showDirectoryPicker' in window && window.directoryHandle) {
                const directoryHandle = window.directoryHandle;
    
                // Função auxiliar para criar subpastas
                async function createDirectoryStructure(pathParts, currentHandle) {
                    for (const part of pathParts) {
                        let subDirectoryHandle;
                        try {
                            subDirectoryHandle = await currentHandle.getDirectoryHandle(part, { create: true });
                        } catch (error) {
                            console.error(`Erro ao criar pasta ${part}:`, error);
                        }
                        currentHandle = subDirectoryHandle;
                    }
                    return currentHandle;
                }
            
                const pathParts = file_name.split('/');
                const baseDirectory = await createDirectoryStructure(pathParts.slice(0, -1), directoryHandle); // Exclui o nome do arquivo para criar pastas
            
                const fileHandle = await baseDirectory.getFileHandle(pathParts[pathParts.length - 1], { create: true });
                const writable = await fileHandle.createWritable();
                const fileBuffer = new Uint8Array(atob(file_content_base64).split("").map(c => c.charCodeAt(0)));
            
                // Escrever o arquivo diretamente no diretório correto
                await writable.write(fileBuffer);
                await writable.close();


            } else {
                // Caso o FileSystemAccess API não seja suportado, use o download padrão
                const blob = new Blob([new Uint8Array(atob(file_content_base64).split("").map(c => c.charCodeAt(0)))], { type: 'application/octet-stream' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.download = file_name;
                link.click();
                URL.revokeObjectURL(url);
            }
        
            const container = document.createElement('div');
            container.className = "agent-message bg-gray-100 dark:bg-gray-800 p-4 rounded-2xl shadow-md max-w-xs mb-4 flex space-x-4 transition duration-300 hover:shadow-lg";
        
            // Icon container
            const iconContainer = document.createElement('div');
            iconContainer.className = "text-blue-600 text-xl flex-shrink-0";
        
            // Icon logic
            const iconMap = {
                'pdf': 'fa-file-pdf',
                'doc': 'fa-file-word',
                'docx': 'fa-file-word',
                'xls': 'fa-file-excel',
                'xlsx': 'fa-file-excel',
                'ppt': 'fa-file-powerpoint',
                'pptx': 'fa-file-powerpoint',
                'txt': 'fa-file-alt',
                'py': 'fa-python',
                'js': 'fa-js',
                'json': 'fa-brackets-curly',
                'env': 'fa-gear',
                'html': 'fa-code',
                'css': 'fa-paint-brush',
                'zip': 'fa-file-zipper',
                'rar': 'fa-file-zipper',
            };
        
            const iconClass = iconMap[file_extension] || (isImage ? 'fa-image' : 'fa-file-alt');
            iconContainer.innerHTML = `<i class="fas ${iconClass}"></i>`;
        
            const textContainer = document.createElement('div');
            textContainer.className = "flex-1 overflow-hidden";
        
            const link = document.createElement('a');
            link.href = `data:application/octet-stream;base64,${file_content_base64}`;
            link.download = file_name;
            link.textContent = file_name;
            link.className = "text-sm font-medium text-blue-600 hover:underline break-words";
        
            const info = document.createElement('div');
            info.className = "text-xs text-gray-500";
            info.textContent = "File downloaded automatically.";
        
            textContainer.appendChild(link);
            textContainer.appendChild(info);
        
            container.appendChild(iconContainer);
            container.appendChild(textContainer);
        
            // Miniatura de imagem
            if (isImage) {
                const img = document.createElement('img');
                img.src = `data:image/${file_extension};base64,${file_content_base64}`;
                img.alt = file_name;
                img.className = "mt-3 rounded-xl max-w-full max-h-60 border border-gray-300 shadow-sm";
                const imageWrapper = document.createElement('div');
                imageWrapper.className = "w-full";
                imageWrapper.appendChild(img);
                container.appendChild(imageWrapper);
            }
        
            document.getElementById("chat-messages").appendChild(container);
            
            
            // Atualizar o Monaco Editor com o arquivo recebido
            if (window.editor && !isImage) {
                const decodedContent = atob(file_content_base64);

                // Detectar linguagem a partir da extensão do arquivo
                const extensionToLanguage = {
                    'html': 'html',
                    'css': 'css',
                    'js': 'javascript',
                    'json': 'json',
                    'py': 'python',
                    'txt': 'plaintext',
                    'env': 'shell',
                    'md': 'markdown',
                    'java': 'java',
                    'c': 'c',
                    'cpp': 'cpp',
                    'ts': 'typescript',
                };

                const language = extensionToLanguage[file_extension] || 'plaintext';

                // Atualizar conteúdo e linguagem
                editor.setValue(decodedContent);
                monaco.editor.setModelLanguage(editor.getModel(), language);

                // Abrir o painel do editor automaticamente se estiver fechado
                const editorPanel = document.getElementById("code-editor-panel");
                const chatMain = document.getElementById("chat-main");
                if (editorPanel.classList.contains("w-0")) {
                    chatMain.classList.remove("w-full");
                    chatMain.classList.add("md:w-3/5");
                    editorPanel.classList.remove("w-0", "overflow-hidden");
                    editorPanel.classList.add("md:w-2/5");
                }
            }

        }

        if (payload?.type === "agentworkflow") {
            agentWorkflowStep++;
            // addMessage("agent", payload.message);
            // Criação do modal apenas uma vez
            if (!agentWorkflowModal) {
                agentWorkflowModal = document.createElement("div");
                agentWorkflowModal.id = "agent-workflow-modal";
                agentWorkflowModal.className = `chat-message agent-message fade-in-up`;
            
                agentWorkflowModal.innerHTML = `
                    <div class="flex items-start">
                        <img src="static/img/194397500.jpg" class="w-8 h-8 rounded-md object-cover mr-4" alt="agent" />
                        <div class="message-content w-full">
                            <div class="bg-zinc-800 border border-zinc-700 text-white rounded-xl p-4 w-full">
                                <div id="workflow-message" class="text-base font-semibold mb-2 transition-all duration-500">
                                    Inicializando...
                                </div>
                                <div class="w-full h-2 bg-zinc-700 rounded-full overflow-hidden">
                                    <div id="workflow-progress" class="h-full bg-white transition-all duration-500" style="width: 0%;"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            
                document.getElementById("chat-messages").appendChild(agentWorkflowModal);
                agentWorkflowModal.scrollIntoView({ behavior: "smooth" });
            }
            
        
            // Atualiza mensagem com efeito "fall down"
            const messageEl = document.getElementById("workflow-message");
            messageEl.classList.add("opacity-0", "-translate-y-3");
            setTimeout(() => {
                messageEl.textContent = payload.message || "Executando etapa...";
                messageEl.classList.remove("-translate-y-3");
                messageEl.classList.add("translate-y-3");
                messageEl.classList.remove("opacity-0");
            }, 200);
        
            // Atualiza barra de progresso (assumindo um total de 100 etapas)
            const progressEl = document.getElementById("workflow-progress");
            const totalSteps = 100;
            const progressPercentage = Math.min((agentWorkflowStep / totalSteps) * 100, 100);
            progressEl.style.width = `${progressPercentage}%`;

            // Oculta o modal após a última etapa
            if (agentWorkflowStep >= totalSteps) {
                setTimeout(() => {
                    agentWorkflowModal.remove();
                    agentWorkflowModal = null;
                    agentWorkflowStep = 0;
                }, 3000);
            }
        }
        
        if (payload?.type === "usage_summary") {
            const usage = payload.message;
        
            const container = document.createElement('div');
            container.className = "agent-message bg-indigo-50 dark:bg-indigo-900 text-indigo-900 dark:text-white p-4 rounded-2xl shadow-md mb-4 max-w-sm mx-auto space-y-2 border border-indigo-300 dark:border-indigo-700";
        
            const title = document.createElement('div');
            title.className = "text-sm font-semibold mb-1";
            title.textContent = `📊 Token Usage: $${usage.cost_total}`;
        
            const makeRow = (label, value) => {
                const row = document.createElement('div');
                row.className = "flex justify-between text-sm";
                row.innerHTML = `<span class="font-medium">${label}</span><span>${value}</span>`;
                return row;
            };
        
            container.appendChild(title);
            container.appendChild(makeRow("🔤 Input Tokens: ", usage.input_tokens));
            container.appendChild(makeRow("📦 Cached Tokens: ", usage.cached_tokens));
            container.appendChild(makeRow("🧠 Reasoning Tokens: ", usage.reasoning_tokens));
            container.appendChild(makeRow("💬 Completion Tokens: ", usage.completion_tokens));
            container.appendChild(makeRow("🔢 Total Tokens: ", usage.total_tokens));
            container.appendChild(makeRow("💰 Input Token Costs: ", usage.cost_instr));
            container.appendChild(makeRow("💸 Output Token Costs: ", usage.cost_out));

        
            document.getElementById("chat-messages").appendChild(container);
            container.scrollIntoView({ behavior: "smooth" });
        }
        
    });
    
    // Handle connection errors
    socket.on('connect_error', function(error) {
        console.error("Erro de conexão WebSocket:", error);
        removeTypingIndicator();
        
        addMessage("agent", "Desculpe, não foi possível conectar ao serviço de chat. Por favor, tente novamente mais tarde.")
    });
}
