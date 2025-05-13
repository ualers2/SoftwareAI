from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *


class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: FrontEndData):
    print(f"DashboardCRM: {input_data.FrontEndContent}")

              
def DashboardCRM(
                                session_id, 
                                appcompany,
                                path_ProjectWeb,
                                path_html,
                                path_js,
                                path_css,
                                doc_md,
                                Keys_path,


                            ):
   
    os.chdir(path_ProjectWeb)

    ResumocomCardsDinâmicos_HTML = """
            <div id="sales-summary" class="summary-container">
            <div class="summary-card" data-status="total">Total de Leads: <span>0</span></div>
            <div class="summary-card" data-status="negociacao">Em Negociação: <span>0</span></div>
            <div class="summary-card" data-status="convertido">Convertidos: <span>0</span></div>
            <div class="summary-card" data-status="perdido">Perdidos: <span>0</span></div>
            </div>

"""

    ResumocomCardsDinâmicos_JavaScript = """
            function atualizarResumo(leads) {{
            const contadores = {{
                total: leads.length,
                negociacao: leads.filter(l => l.status === 'negociacao').length,
                convertido: leads.filter(l => l.status === 'convertido').length,
                perdido: leads.filter(l => l.status === 'perdido').length
            }};

            document.querySelectorAll('.summary-card').forEach(card => {{
                const status = card.dataset.status;
                card.querySelector('span').textContent = contadores[status];
            }});
            }}

"""

    ResumocomCardsDinâmicos_CSS = """
            .summary-container {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1rem;
            }}
            .summary-card {{
            background: #f1f1f1;
            padding: 1rem;
            border-radius: 8px;
            font-weight: bold;
            }}


"""

    KanbanInterativo_HTML = """
            <div id="kanban" class="kanban-board">
            <div class="kanban-column" data-status="negociacao"><h3>Em Negociação</h3></div>
            <div class="kanban-column" data-status="convertido"><h3>Convertidos</h3></div>
            <div class="kanban-column" data-status="perdido"><h3>Perdidos</h3></div>
            </div>


"""

    KanbanInterativo_JavaScript = """
            function criarLeadCard(lead) {{
            const card = document.createElement('div');
            card.className = 'lead-card';
            card.textContent = lead.nome;
            card.draggable = true;
            card.dataset.id = lead.id;

            card.addEventListener('dragstart', e => {{
                e.dataTransfer.setData('id', lead.id);
            }});

            return card;
            }}

            function carregarKanban(leads) {{
            document.querySelectorAll('.kanban-column').forEach(col => {{
                col.innerHTML = `<h3>${{col.querySelector('h3').textContent}}</h3>`; // reset
                const status = col.dataset.status;
                leads.filter(l => l.status === status).forEach(lead => {{
                col.appendChild(criarLeadCard(lead));
                }});
            }});
            }}

            document.querySelectorAll('.kanban-column').forEach(col => {{
            col.addEventListener('dragover', e => e.preventDefault());
            col.addEventListener('drop', e => {{
                const id = e.dataTransfer.getData('id');
                const status = col.dataset.status;
                const lead = leads.find(l => l.id == id);
                lead.status = status;
                carregarKanban(leads);
                atualizarResumo(leads);
            }});
            }});
"""

    KanbanInterativo_CSS = """
            .kanban-board {{
            display: flex;
            gap: 1rem;
            }}
            .kanban-column {{
            flex: 1;
            background: #e9ecef;
            padding: 1rem;
            border-radius: 8px;
            min-height: 200px;
            }}
            .lead-card {{
            background: #fff;
            padding: 0.5rem;
            margin: 0.5rem 0;
            border: 1px solid #ccc;
            border-radius: 6px;
            cursor: grab;
            }}

"""

    CadastrodeLead_HTML = """
            <button onclick="abrirModal()">Novo Lead</button>
            <div id="leadModal" class="modal hidden">
            <div class="modal-content">
                <h2>Novo Lead</h2>
                <input type="text" id="leadNome" placeholder="Nome do Lead" />
                <select id="leadStatus">
                <option value="negociacao">Em Negociação</option>
                <option value="convertido">Convertido</option>
                <option value="perdido">Perdido</option>
                </select>
                <button onclick="salvarLead()">Salvar</button>
                <button onclick="fecharModal()">Cancelar</button>
            </div>
            </div>

"""

    CadastrodeLead_JavaScript = """

            let leads = [];

            function abrirModal() {{
            document.getElementById('leadModal').classList.remove('hidden');
            }}

            function fecharModal() {{
            document.getElementById('leadModal').classList.add('hidden');
            }}

            function salvarLead() {{
            const nome = document.getElementById('leadNome').value;
            const status = document.getElementById('leadStatus').value;
            if (!nome) return alert("Nome obrigatório");

            const novoLead = {{
                id: Date.now(),
                nome,
                status
            }};

            leads.push(novoLead);
            carregarKanban(leads);
            atualizarResumo(leads);
            fecharModal();
            }}

"""

    CadastrodeLead_CSS = """

            .modal.hidden {{
            display: none;
            }}
            .modal {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            }}
            .modal-content {{
            background: #fff;
            padding: 2rem;
            border-radius: 8px;
            }}

"""

    TabeladeClientes_HTML = """

            <table id="clientesFechados">
            <thead>
                <tr>
                <th>Nome</th>
                <th>Valor</th>
                <th>Data</th>
                <th>Ações</th>
                </tr>
            </thead>
            <tbody></tbody>
            </table>
"""

    TabeladeClientes_JavaScript = """

            function atualizarTabelaClientes(leads) {{
            const tbody = document.querySelector('#clientesFechados tbody');
            tbody.innerHTML = '';

            leads.filter(l => l.status === 'convertido').forEach(lead => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                <td>${{lead.nome}}</td>
                <td>R$ ${{(lead.valor || 0).toFixed(2)}}</td>
                <td>${{lead.data || new Date().toLocaleDateString()}}</td>
                <td><button onclick="alert('Detalhes de ${{lead.nome}}')">Ver</button></td>
                `;
                tbody.appendChild(tr);
            }});
            }}
"""

    IndicadoresDinâmicos_HTML = """
            <div id="clientes-summary" class="summary-container">
            <div class="summary-card" data-indicador="total">Total de Clientes: <span>0</span></div>
            <div class="summary-card" data-indicador="ativos">Ativos: <span>0</span></div>
            <div class="summary-card" data-indicador="inativos">Inativos: <span>0</span></div>
            <div class="summary-card" data-indicador="ultimo">Último Adicionado: <span>-</span></div>
            </div>
"""
    
    IndicadoresDinâmicos_JavaScript = """

            function atualizarIndicadoresClientes(clientes) {{
            const total = clientes.length;
            const ativos = clientes.filter(c => c.ativo).length;
            const inativos = total - ativos;
            const ultimo = clientes.length ? clientes[clientes.length - 1].nome : '-';

            const indicadores = {{
                total,
                ativos,
                inativos,
                ultimo
            }};

            document.querySelectorAll('#clientes-summary .summary-card').forEach(card => {{
                const tipo = card.dataset.indicador;
                card.querySelector('span').textContent = indicadores[tipo];
            }});
            }}
"""

    TabelaDetalhada_HTML = """
            <table id="tabelaClientes">
            <thead>
                <tr>
                <th>Nome</th>
                <th>Email</th>
                <th>Status</th>
                <th>Telefone</th>
                <th>Ações</th>
                </tr>
            </thead>
            <tbody></tbody>
            </table>
"""
    
    TabelaDetalhada_JavaScript = """
            function renderizarTabelaClientes(clientes) {{
            const tbody = document.querySelector('#tabelaClientes tbody');
            tbody.innerHTML = '';

            clientes.forEach(cliente => {{
                const tr = document.createElement('tr');
                tr.innerHTML = `
                <td>${{cliente.nome}}</td>
                <td>${{cliente.email}}</td>
                <td>${{cliente.ativo ? 'Ativo' : 'Inativo'}}</td>
                <td>${{cliente.telefone}}</td>
                <td>
                    <button onclick="verHistorico('${{cliente.id}}')">Histórico</button>
                    <button onclick="editarCliente('${{cliente.id}}')">Editar</button>
                    <button onclick="excluirCliente('${{cliente.id}}')">Excluir</button>
                </td>
                `;
                tbody.appendChild(tr);
            }});
            }}
"""

    CadastrodeCliente_HTML = """
            <button onclick="abrirModalCliente()">Novo Cliente</button>
            <div id="clienteModal" class="modal hidden">
            <div class="modal-content">
                <h2>Novo Cliente</h2>
                <input type="text" id="clienteNome" placeholder="Nome" />
                <input type="email" id="clienteEmail" placeholder="Email" />
                <input type="text" id="clienteTelefone" placeholder="Telefone" />
                <label><input type="checkbox" id="clienteAtivo" checked /> Ativo</label>
                <button onclick="salvarCliente()">Salvar</button>
                <button onclick="fecharModalCliente()">Cancelar</button>
            </div>
            </div>
"""
    
    CadastrodeCliente_JavaScript = """
            let clientes = [];
            function abrirModalCliente() {{
            document.getElementById('clienteModal').classList.remove('hidden');
            }}
            function fecharModalCliente() {{
            document.getElementById('clienteModal').classList.add('hidden');
            }}
            function salvarCliente() {{
            const nome = document.getElementById('clienteNome').value;
            const email = document.getElementById('clienteEmail').value;
            const telefone = document.getElementById('clienteTelefone').value;
            const ativo = document.getElementById('clienteAtivo').checked;
            if (!nome || !email) return alert("Nome e Email obrigatórios");
            const novoCliente = {{
                id: Date.now().toString(),
                nome,
                email,
                telefone,
                ativo
            }};
            clientes.push(novoCliente);
            atualizarIndicadoresClientes(clientes);
            renderizarTabelaClientes(clientes);
            fecharModalCliente();
            }}
"""

    AçõesdeEdiçãoExclusãoeHistórico_JavaScript = """
            function editarCliente(id) {{
            const cliente = clientes.find(c => c.id === id);
            if (!cliente) return;

            document.getElementById('clienteNome').value = cliente.nome;
            document.getElementById('clienteEmail').value = cliente.email;
            document.getElementById('clienteTelefone').value = cliente.telefone;
            document.getElementById('clienteAtivo').checked = cliente.ativo;

            abrirModalCliente();

            salvarCliente = function () {{
                cliente.nome = document.getElementById('clienteNome').value;
                cliente.email = document.getElementById('clienteEmail').value;
                cliente.telefone = document.getElementById('clienteTelefone').value;
                cliente.ativo = document.getElementById('clienteAtivo').checked;

                atualizarIndicadoresClientes(clientes);
                renderizarTabelaClientes(clientes);
                fecharModalCliente();

                salvarCliente = originalSalvarCliente; // volta função original
            }};
            }}

            const originalSalvarCliente = salvarCliente;

            function excluirCliente(id) {{
            clientes = clientes.filter(c => c.id !== id);
            atualizarIndicadoresClientes(clientes);
            renderizarTabelaClientes(clientes);
            }}

            function verHistorico(id) {{
            alert(`Exibindo histórico do cliente ${{id}}`);
            }}

"""

    ListadeFollowupsAgendados_HTML = """
            <section id="followup-section">
                <h2>Follow-ups Agendados</h2>
                <ul id="listaFollowups"></ul>
            </section>
"""
    
    ListadeFollowupsAgendados_JavaScript = """
            let followups = [];
            function renderizarFollowups() {{
            const ul = document.getElementById('listaFollowups');
            ul.innerHTML = '';
            followups.forEach(f => {{
                const li = document.createElement('li');
                li.innerHTML = `
                <strong>${{f.nome}}</strong> - ${{f.email}}<br>
                <small>Agendado para: ${{new Date(f.data).toLocaleString()}}</small><br>
                <button onclick="enviarEmailFollowup('${{f.id}}')">Enviar Agora</button>
                <button onclick="cancelarFollowup('${{f.id}}')">Cancelar</button>
                `;
                ul.appendChild(li);
            }});
            }}
"""

    FormulárioparaAgendarNovoFollowup_HTML = """
            <button onclick="abrirModalFollowup()">Novo Follow-up</button>
            <div id="modalFollowup" class="modal hidden">
            <div class="modal-content">
                <h3>Agendar Follow-up</h3>
                <input type="text" id="fupNome" placeholder="Nome do Contato" />
                <input type="email" id="fupEmail" placeholder="Email" />
                <input type="datetime-local" id="fupData" />
                <textarea id="fupMensagem" placeholder="Mensagem do Follow-up"></textarea>
                <button onclick="salvarFollowup()">Salvar</button>
                <button onclick="fecharModalFollowup()">Cancelar</button>
            </div>
            </div>
"""
    
    FormulárioparaAgendarNovoFollowup_JavaScript = """

            function abrirModalFollowup() {{
            document.getElementById('modalFollowup').classList.remove('hidden');
            }}
            function fecharModalFollowup() {{
            document.getElementById('modalFollowup').classList.add('hidden');
            }}

            function salvarFollowup() {{
            const nome = document.getElementById('fupNome').value;
            const email = document.getElementById('fupEmail').value;
            const data = document.getElementById('fupData').value;
            const mensagem = document.getElementById('fupMensagem').value;

            if (!nome || !email || !data || !mensagem) return alert('Preencha todos os campos');

            const novoFollowup = {{
                id: Date.now().toString(),
                nome,
                email,
                data,
                mensagem,
                enviado: false
            }};

            followups.push(novoFollowup);
            renderizarFollowups();
            fecharModalFollowup();
            }}
"""

    EnvioSimuladodeEmail_JavaScript = """

            function enviarEmailFollowup(id) {{
            const f = followups.find(f => f.id === id);
            if (!f) return;

            f.enviado = true;
            alert(`Email enviado para ${{f.email}}:\n\n${{f.mensagem}}`);
            renderizarFollowups();
            }}
"""

    CancelamentodeFollowup_JavaScript = """
            function cancelarFollowup(id) {{
            followups = followups.filter(f => f.id !== id);
            renderizarFollowups();
            }}
            
"""

    DisparadordeAgendamentos_JavaScript = """
            setInterval(() => {{
            const agora = new Date();
            followups.forEach(f => {{
                const agendado = new Date(f.data);
                if (!f.enviado && agendado <= agora) {{
                enviarEmailFollowup(f.id);
                }}
            }});
            }}, 60000); // verifica a cada 60s
            
"""

    AutomaçãodeFollowups_CSS = """
            .modal {{
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5);
            display: flex; justify-content: center; align-items: center;
            }}
            .modal-content {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            }}
            .hidden {{ display: none; }}
            #listaFollowups li {{
            margin: 10px 0;
            background: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
            }}

    """

    IndicadoresChavedePerformance_HTML = """
            <section id="relatorios-metas">
            <h2>Relatórios e Metas</h2>
            <div id="indicadores-kpi" class="kpis">
                <div class="kpi" id="vendasTotais">Vendas Totais: R$ 0</div>
                <div class="kpi" id="metasAtingidas">Metas Atingidas: 0</div>
                <div class="kpi" id="taxaConversao">Taxa de Conversão: 0%</div>
            </div>
            <canvas id="graficoVendas" width="600" height="300"></canvas>
            </section>
"""
    
    IndicadoresChavedePerformance_JavaScript = """

            const desempenhoEquipe = {{
            vendasTotais: 35000,
            metasAtingidas: 4,
            totalLeads: 130,
            totalClientes: 52
            }};

            function atualizarIndicadores() {{
            document.getElementById("vendasTotais").textContent = `Vendas Totais: R$ ${{desempenhoEquipe.vendasTotais.toLocaleString()}}`;
            document.getElementById("metasAtingidas").textContent = `Metas Atingidas: ${{desempenhoEquipe.metasAtingidas}}`;
            const taxa = (desempenhoEquipe.totalClientes / desempenhoEquipe.totalLeads * 100).toFixed(1);
            document.getElementById("taxaConversao").textContent = `Taxa de Conversão: ${{taxa}}%`;
            }}

            atualizarIndicadores();

"""

    GráficodeDesempenhoMensal_JavaScript = """

            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
            const ctx = document.getElementById('graficoVendas').getContext('2d');
            const graficoVendas = new Chart(ctx, {{
                type: 'bar',
                data: {{
                labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
                datasets: [{{
                    label: 'Vendas (R$)',
                    data: [5000, 7000, 8500, 9200, 5300],
                    backgroundColor: '#4CAF50'
                }}]
                }},
                options: {{
                responsive: true,
                plugins: {{
                    legend: {{ display: false }},
                    title: {{
                    display: true,
                    text: 'Desempenho Mensal de Vendas'
                    }}
                }},
                scales: {{
                    y: {{
                    beginAtZero: true
                    }}
                }}
                }}
            }});
            </script>

"""

    TabeladeMetasporColaborador_HTML= """

            <h3>Metas por Colaborador</h3>
            <table id="tabelaMetas">
            <thead>
                <tr>
                <th>Nome</th>
                <th>Meta (R$)</th>
                <th>Vendido</th>
                <th>Progresso</th>
                </tr>
            </thead>
            <tbody></tbody>
            </table>
"""

    TabeladeMetasporColaborador_JavaScript= """

            const metas = [
            {{ nome: 'Ana', meta: 10000, vendido: 8500 }},
            {{ nome: 'Carlos', meta: 12000, vendido: 12200 }},
            {{ nome: 'Juliana', meta: 8000, vendido: 4000 }},
            ];

            function renderizarTabelaMetas() {{
            const tbody = document.querySelector("#tabelaMetas tbody");
            tbody.innerHTML = "";

            metas.forEach(m => {{
                const tr = document.createElement("tr");
                const progresso = (m.vendido / m.meta * 100).toFixed(1);

                tr.innerHTML = `
                <td>${{m.nome}}</td>
                <td>R$ ${{m.meta.toLocaleString()}}</td>
                <td>R$ ${{m.vendido.toLocaleString()}}</td>
                <td>
                    <div style="background:#eee;width:100%;height:10px;border-radius:5px;">
                    <div style="width:${{progresso}}%;height:100%;background:#4CAF50;border-radius:5px;"></div>
                    </div>
                    <small>${{progresso}}%</small>
                </td>
                `;
                tbody.appendChild(tr);
            }});
            }}

            renderizarTabelaMetas();
"""

    SeçãoRelatórioseMetas_CSS ="""

            .kpis {{
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            }}
            .kpi {{
            background: #f0f0f0;
            padding: 15px;
            border-radius: 10px;
            font-weight: bold;
            }}
            #tabelaMetas {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            }}
            #tabelaMetas th, #tabelaMetas td {{
            border: 1px solid #ddd;
            padding: 8px;
            }}
            #tabelaMetas th {{
            background-color: #f8f8f8;
            }}

"""




    agent_ids = ['CRM']
    agents_metadata = EgetMetadataAgent(agent_ids)

    name = agents_metadata[f'{agent_ids[0]}']["name"]
    model = agents_metadata[f'{agent_ids[0]}']["model"]
    instruction = agents_metadata[f'{agent_ids[0]}']["instruction"]
    try:
      tools = agents_metadata[f'{agent_ids[0]}']["tools"]
      Tools_Name_dict = Egetoolsv2(list(tools))
    except:
      pass

    instruction_formatado = format_instruction(instruction, locals())

    agent = Agent(
        name=str(name),
        instructions=f"""
        {instruction_formatado}        
        """,
        model=str(model),
        tools=Tools_Name_dict,
        # handoffs=[handoff_obj_CodeDockerFileAgent],
    )

    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj