from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *


# from AgentsWorkFlow.Saas.Code.DevOps.DockerFile.Integration import CodeDockerFileAgent


class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[None], input_data: FrontEndData):
    print(f"DashboardReservationPlatformAgent: {input_data.FrontEndContent}")

              
def DashboardReservationPlatformAgent(
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

    CalendárioInterativocomSlotsdeHorários_HTML = """
```html
<div id="reservaCalendario" class="calendario-container">
<!-- Slots gerados dinamicamente -->
</div>
```
"""
   
    CalendárioInterativocomSlotsdeHorários_JavaScript = """
```js
function gerarSlots(horarios, reservas) {{
const container = document.getElementById('reservaCalendario');
container.innerHTML = '';

horarios.forEach(hora => {{
    const slot = document.createElement('div');
    slot.className = 'calendario-slot';
    const reserva = reservas.find(r => r.horario === hora);

    if (reserva) {{
    slot.textContent = `Reservado: ${{reserva.nomeCliente}}`;
    slot.classList.add('ocupado');
    }} else {{
    slot.textContent = `${{hora}} - Disponível`;
    slot.classList.add('disponivel');
    slot.onclick = () => abrirModalReserva(hora);
    }}

    container.appendChild(slot);
}});
}}
```

"""
    
    CalendárioInterativocomSlotsdeHorários_CSS = """
```css
.calendario-container {{
display: grid;
grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
gap: 1rem;
}}
.calendario-slot {{
padding: 1rem;
background: #e0f7fa;
border-radius: 8px;
cursor: pointer;
}}
.calendario-slot.ocupado {{
background: #ffcdd2;
cursor: not-allowed;
}}
.calendario-slot.disponivel:hover {{
background: #a5d6a7;
}}
```

"""

    ResumodeOcupação_HTML = """
```html
<div id="resumoReservas" class="summary-container">
<div class="summary-card" data-info="total">Total de Slots: <span>0</span></div>
<div class="summary-card" data-info="ocupado">Ocupados: <span>0</span></div>
<div class="summary-card" data-info="disponivel">Disponíveis: <span>0</span></div>
</div>
```

"""

    ResumodeOcupação_JavaScript = """
```js
function atualizarResumoReservas(horarios, reservas) {{
const total = horarios.length;
const ocupado = reservas.length;
const disponivel = total - ocupado;

const dados = {{ total, ocupado, disponivel }};
document.querySelectorAll('#resumoReservas .summary-card').forEach(card => {{
    const tipo = card.dataset.info;
    card.querySelector('span').textContent = dados[tipo];
}});
}}
```

"""

    ModaldeNovaReserva_HTML = """
```html
<div id="reservaModal" class="modal hidden">
<div class="modal-content">
    <h2>Nova Reserva</h2>
    <input type="text" id="nomeCliente" placeholder="Nome do Cliente" />
    <input type="text" id="valorReserva" placeholder="Valor (R$)" />
    <input type="hidden" id="horarioSelecionado" />
    <button onclick="salvarReserva()">Salvar</button>
    <button onclick="fecharModalReserva()">Cancelar</button>
</div>
</div>
```


"""

    ModaldeNovaReserva_JavaScript = """
```js
let reservas = [];

function abrirModalReserva(horario) {{
document.getElementById('reservaModal').classList.remove('hidden');
document.getElementById('horarioSelecionado').value = horario;
}}
function fecharModalReserva() {{
document.getElementById('reservaModal').classList.add('hidden');
}}
function salvarReserva() {{
const nome = document.getElementById('nomeCliente').value;
const valor = parseFloat(document.getElementById('valorReserva').value);
const horario = document.getElementById('horarioSelecionado').value;

if (!nome || isNaN(valor)) return alert("Preencha todos os campos");

reservas.push({{ nomeCliente: nome, valor, horario }});
gerarSlots(horarios, reservas);
atualizarResumoReservas(horarios, reservas);
atualizarTabelaPagamentos(reservas);
fecharModalReserva();
}}
```
"""

    IndicadoresdeClientes_HTML = """
```html
<div id="clientesReservasResumo" class="summary-container">
<div class="summary-card" data-indicador="total">Total de Clientes: <span>0</span></div>
<div class="summary-card" data-indicador="ultimo">Último Cliente: <span>-</span></div>
</div>
```


"""

    IndicadoresdeClientes_JavaScript = """
```js
function atualizarResumoClientesReservas(reservas) {{
const nomesUnicos = [...new Set(reservas.map(r => r.nomeCliente))];
const ultimo = reservas.length ? reservas[reservas.length - 1].nomeCliente : '-';

document.querySelector('[data-indicador="total"] span').textContent = nomesUnicos.length;
document.querySelector('[data-indicador="ultimo"] span').textContent = ultimo;
}}
```
"""

    TabeladeClientescomHistórico_HTML = """
```html
<table id="tabelaClientesReservas">
<thead>
    <tr>
    <th>Nome</th>
    <th>Reservas</th>
    <th>Total Pago</th>
    <th>Ações</th>
    </tr>
</thead>
<tbody></tbody>
</table>
```

"""

    TabeladeClientescomHistórico_JavaScript = """
```js
function gerarTabelaClientesReservas(reservas) {{
const tabela = document.querySelector('#tabelaClientesReservas tbody');
tabela.innerHTML = '';

const agrupado = {{}};
reservas.forEach(r => {{
    if (!agrupado[r.nomeCliente]) {{
    agrupado[r.nomeCliente] = {{ total: 0, count: 0 }};
    }}
    agrupado[r.nomeCliente].total += r.valor;
    agrupado[r.nomeCliente].count += 1;
}});

Object.keys(agrupado).forEach(nome => {{
    const tr = document.createElement('tr');
    const dados = agrupado[nome];
    tr.innerHTML = `
    <td>${{nome}}</td>
    <td>${{dados.count}}</td>
    <td>R$ ${{dados.total.toFixed(2)}}</td>
    <td><button onclick="alert('Ver histórico de ${{nome}}')">Ver</button></td>
    `;
    tabela.appendChild(tr);
}});
}}
```
"""

    TabeladePagamentos_HTML = """
```html
<table id="tabelaPagamentos">
<thead>
    <tr>
    <th>Cliente</th>
    <th>Horário</th>
    <th>Valor</th>
    <th>Data</th>
    </tr>
</thead>
<tbody></tbody>
</table>
```

"""

    TabeladeClientescomHistórico_JavaScript = """
```js
function atualizarTabelaPagamentos(reservas) {{
const tbody = document.querySelector('#tabelaPagamentos tbody');
tbody.innerHTML = '';

reservas.forEach(r => {{
    const tr = document.createElement('tr');
    tr.innerHTML = `
    <td>${{r.nomeCliente}}</td>
    <td>${{r.horario}}</td>
    <td>R$ ${{r.valor.toFixed(2)}}</td>
    <td>${{new Date().toLocaleDateString()}}</td>
    `;
    tbody.appendChild(tr);
}});
}}
```
"""


    agent_ids = ['ReservationPlatform']
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
        # handoffs=[handoff_obj_CodeTransferAgent],
    )

    

    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj