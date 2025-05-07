
window.allTools = [];

// Funções para abrir e fechar o modal
function abrirModal(id) {
    const modal = document.getElementById(id);
    modal.classList.remove('hidden');
    hljs.highlightAll(); // aplica highlight no código ao abrir
}

function fecharModal(id) {
    const modal = document.getElementById(id);
    modal.classList.add('hidden');
}
function escapeForJsString(str) {
    return str.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\$/g, '\\$');
}

function copiarTexto(texto, botao) {
    navigator.clipboard.writeText(texto).then(() => {
        const tooltip = botao.nextElementSibling;
        tooltip.classList.remove('opacity-0');
        tooltip.classList.add('opacity-100');

        setTimeout(() => {
            tooltip.classList.remove('opacity-100');
            tooltip.classList.add('opacity-0');
        }, 1500);
    }).catch(err => {
        console.error('Erro ao copiar texto:', err);
    });
}
async function carregarFerramentas() {
    const resposta = await fetch('https://softwareai-library-hub.rshare.io/api/list-tools');
    const ferramentas = await resposta.json();
    window.allTools = ferramentas;
    renderTools(ferramentas);
    updateFilterCounts();  // atualiza contagem após carregar 
}


function renderTools(tools) {
    const container = document.getElementById('tools-container');
    container.innerHTML = '';
  
    tools.forEach(tool => {
        const card = document.createElement('div');
        card.className = 'bg-white shadow rounded-xl p-5 border hover:border-blue-500 transition-all';

        const modalId = `modal-${tool.id}`;
        const pipCommand = `pip install softwareai-engine-library`;
        const pythonCode = `from softwareai_engine_library.EngineProcess.EgetTools import Egetoolsv2\nimported_tools = Egetoolsv2(functionstools = ['${tool.id}'])`;

        const pythonCodewithApi_import_libs = `import requests\nimport yaml\nimport os\nimport json\nimport zipfile\nimport importlib`;

        const pythonCodewithApi_download_tools_with_api = `def download_tools_zip(tool_ids: list, output_path: str = 'tools_code.zip', base_url: str = 'https://softwareai-library-hub.rshare.io') -> bool:\n    joined_ids = ','.join(tool_ids)\n    url = f'{base_url}/api/tool-code/{joined_ids}'\n    try:\n        response = requests.get(url)\n        if response.status_code == 200:\n            with open(output_path, 'wb') as f:\n                f.write(response.content)\n            print(f\"ZIP baixado com sucesso: {output_path}\")\n            extract_dir = os.path.join(os.path.dirname(__file__), 'Functions')\n            os.makedirs(extract_dir, exist_ok=True)\n            with zipfile.ZipFile(output_path, 'r') as zip_ref:\n                zip_ref.extractall(extract_dir)\n            print(f\"Arquivos extraídos para: {extract_dir}\")\n            return True\n        else:\n            print(f\"Erro {response.status_code}: {response.json()}\")\n            return False\n    except Exception as e:\n        print(f\"Erro durante o download ou extração: {e}\")\n        return False`;

        const pythonCodewithApi_import_tool = `def import_tool(tool_name: str, base_dir: str = 'Functions'):\n    module_path = os.path.join(base_dir, tool_name, f\"{tool_name}.py\")\n    spec = importlib.util.spec_from_file_location(tool_name, module_path)\n    if spec and spec.loader:\n        module = importlib.util.module_from_spec(spec)\n        spec.loader.exec_module(module)\n        for attr_name in dir(module):\n            attr = getattr(module, attr_name)\n            if hasattr(attr, \"name\") and hasattr(attr, \"description\"):\n                return attr\n        raise ImportError(f\"Nenhuma função decorada com @function_tool encontrada em {tool_name}.py\")\n    else:\n        raise ImportError(f\"Não foi possível importar a ferramenta: {tool_name}\")`;

        const pythonCodewithApi = `def Egetoolsv2(functionstools = ['${tool.id}']):\n    os.chdir(os.path.dirname(__file__))\n    tools = functionstools\n    download_tools_zip(tools)\n    os.remove(\"tools_code.zip\")\n    imported_tools = [import_tool(tool) for tool in tools]\n    print(imported_tools)\n    return imported_tools`;
        let planClasses;
        switch (tool.type_plan) {
            case 'free':
                planClasses = 'bg-green-500 text-white';
                break;
            case 'premium':
                planClasses = 'bg-blue-500 text-white';
                break;
            default:
                planClasses = 'bg-gray-200 text-gray-800';
        }
        card.innerHTML = `

            <div class="flex items-center space-x-2 mb-2">
                <i class="${tool.icon} text-blue-600"></i>
                <h2 class="text-lg font-semibold">${tool.name}</h2>
                <span class="text-xs ${planClasses} px-2 py-0.5 rounded-full">
                  ${tool.type_plan}
                </span>
            </div>
            <p class="text-sm text-gray-600 mb-2">${tool.shortDescription}</p>
            <p class="text-xs text-gray-500 mb-2">${tool.fullDescription}</p>
            <div class="flex gap-4 mt-2">
                <button class="text-sm text-blue-600 underline hover:text-blue-800" onclick="event.stopPropagation(); abrirModal('${modalId}')">View api request</button>
                <button class="text-sm text-gray-600 underline hover:text-gray-800" onclick="window.location.href='/tools/${tool.id}'">View Code and Metadata</button>
            </div>
            <!-- Modal -->
            <div id="${modalId}" class="modal hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div class="bg-white p-6 rounded-lg shadow-lg max-w-xl w-full relative overflow-y-auto max-h-[80vh]" onclick="event.stopPropagation();">
                    <button onclick="fecharModal('${modalId}')" class="absolute top-2 right-2 text-gray-500 hover:text-black text-xl">&times;</button>
                    <h3 class="text-lg font-semibold mb-4">How to use this tool with our python package, useful for those who want to integrate quickly</h3>


                    <p class="text-sm mb-1 text-gray-700 flex items-center">
                        Install the required library with:
                        <button onclick="copiarTexto('${pipCommand}', this)" class="text-xs text-blue-600 hover:underline ml-2 relative">
                            📋 Copy library
                        </button>
                        <span class="absolute left-full ml-2 text-xs bg-black text-white rounded px-2 py-0.5 opacity-0 transition-opacity duration-300">Copied!</span>
                    </p>
                    <pre class="bg-gray-100 p-3 rounded text-sm text-gray-800 mb-2"><code class="language-bash">${pipCommand}</code></pre>

                    <p class="text-sm mb-1 text-gray-700 flex items-center">
                        Code to import the tool via python package:
                        <button onclick="copiarTexto(\`${pythonCode}\`, this)" class="text-xs text-blue-600 hover:underline ml-2 relative">
                            📋 Copy code
                        </button>
                        <span class="absolute left-full ml-2 text-xs bg-black text-white rounded px-2 py-0.5 opacity-0 transition-opacity duration-300">Copied!</span>
                    </p>
                    <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-[400px] text-gray-800">
                        <code class="language-python">${pythonCode}</code>
                    </pre>

                    <h3 class="text-lg font-semibold mb-4">How to use this tool directly via API, useful for those who want to make their own integrations and/or languages</h3>
                    
                    <p class="text-sm mb-1 text-gray-700 flex items-center">
                        1) Primeiro importar pacotes python necessarios:
                        <button data-code="${pythonCodewithApi_import_libs}" onclick="copiarTexto(this.dataset.code, this)" class="text-xs text-blue-600 hover:underline ml-2 relative">
                            📋 Copy code
                        </button>
                        <span class="absolute left-full ml-2 text-xs bg-black text-white rounded px-2 py-0.5 opacity-0 transition-opacity duration-300">Copied!</span>
                    </p>
                    <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-[400px] text-gray-800">
                        <code class="language-python">${pythonCodewithApi_import_libs}</code>
                    </pre>
                    
                    <p class="text-sm mb-1 text-gray-700 flex items-center">
                        2) Segundo Fazer o download de ferramentas:
                        <button data-code="${pythonCodewithApi_download_tools_with_api}" onclick="copiarTexto(this.dataset.code, this)" class="text-xs text-blue-600 hover:underline ml-2 relative">
                            📋 Copy code
                        </button>
                        <span class="absolute left-full ml-2 text-xs bg-black text-white rounded px-2 py-0.5 opacity-0 transition-opacity duration-300">Copied!</span>
                    </p>
                    <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-[400px] text-gray-800">
                        <code class="language-python">${pythonCodewithApi_download_tools_with_api}</code>
                    </pre>

                    
                    <p class="text-sm mb-1 text-gray-700 flex items-center">
                        3) Terceiro Fazer a importacao de ferramentas com função decorada @function_tool:
                        <button data-code="${pythonCodewithApi_import_tool}" onclick="copiarTexto(this.dataset.code, this)" class="text-xs text-blue-600 hover:underline ml-2 relative">
                            📋 Copy code
                        </button>
                        <span class="absolute left-full ml-2 text-xs bg-black text-white rounded px-2 py-0.5 opacity-0 transition-opacity duration-300">Copied!</span>
                    </p>
                    <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-[400px] text-gray-800">
                        <code class="language-python">${pythonCodewithApi_import_tool}</code>
                    </pre>
                    
                    <p class="text-sm mb-1 text-gray-700 flex items-center">
                        4) Quarto Fazer a utilizacao das funcoes de download e importacao:
                        <button data-code="${pythonCodewithApi}" onclick="copiarTexto(this.dataset.code, this)" class="text-xs text-blue-600 hover:underline ml-2 relative">
                            📋 Copy code
                        </button>
                        <span class="absolute left-full ml-2 text-xs bg-black text-white rounded px-2 py-0.5 opacity-0 transition-opacity duration-300">Copied!</span>
                    </p>
                    <pre class="bg-gray-100 p-4 rounded text-sm overflow-auto max-h-[400px] text-gray-800">
                        <code class="language-python">${pythonCodewithApi}</code>
                    </pre>
                </div>
            </div>

        `;

        container.appendChild(card);

        // Evento para fechar o modal ao clicar fora
        setTimeout(() => {
            const modal = document.getElementById(modalId);
            modal.addEventListener('click', () => fecharModal(modalId));
        }, 0);
    });
}
/**
 * Atualiza o texto do select com o número de ferramentas por plano
 */
function updateFilterCounts() {
    const select = document.getElementById('plan-filter');
    const totalFree = window.allTools.filter(t => t.type_plan.toLowerCase() === 'free').length;
    const totalPremium = window.allTools.filter(t => t.type_plan.toLowerCase() === 'premium').length;
    const totalAll = totalFree + totalPremium;
    // Atualiza as opções do select
    select.options[0].text = `All (${totalAll})`;
    select.options[1].text = `Free (${totalFree})`;
    select.options[2].text = `Premium (${totalPremium})`;
}
/**
 * Lê search input e select, filtra allTools e renderiza o resultado
 */
function applyFilters() {
    const searchValue = document.getElementById('search-input').value.toLowerCase();
    const planValue = document.getElementById('plan-filter').value;
  
    const filtered = window.allTools.filter(tool => {
      const matchesName = tool.name.toLowerCase().includes(searchValue);
      const matchesPlan = planValue === 'all' || tool.type_plan.toLowerCase() === planValue;
      return matchesName && matchesPlan;
    });
  
    renderTools(filtered);
  }

/**
 * Conecta eventos de input e change aos filtros
 */
function setupFilters() {
document.getElementById('search-input').addEventListener('input', applyFilters);
document.getElementById('plan-filter').addEventListener('change', applyFilters);
}
