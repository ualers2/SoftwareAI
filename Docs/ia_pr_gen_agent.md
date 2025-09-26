# Documentação Completa — IA PrGen (Agent)

> Arquivo base: agente `PrGen` (implementação em Python fornecida)

---

## Sumário

1. Visão Geral
2. Arquitetura e componentes
3. Dependências e variáveis de ambiente
4. Tipos e contratos (entrada/saída)
5. Fluxo de execução detalhado
6. Prompting: templates e diretrizes
7. Chunking / divisão de input
8. Integração com runner/agents
9. Tratamento de erros, logs e observabilidade
10. Segurança e privacidade
11. Custos estimados e uso de tokens
12. Testes e estratégias de validação
13. Limitações conhecidas e riscos
14. Melhorias e próximos passos
15. Exemplos de uso (snippets)

---

## 1. Visão Geral

`PrGen` é um componente assíncrono responsável por transformar diffs de código (conteúdo de Pull Requests) em:
- um **título de PR** sucinto e informativo; e
- um **corpo de PR** estruturado (Descrição, Mudanças Principais, Por que, Como testar, Observações).

O agente foi desenhado para rodar com modelos de LLM (por padrão `gpt-4.1-nano`) via um framework local de agentes (`agents.Agent`, `Runner`, etc.). Apoia chunking automático quando o diff excede um limite de bytes para contornar limites de contexto.


## 2. Arquitetura e componentes

Principais componentes usados no código:

- `Agent` — classe que encapsula instruções, nome e tipo de saída (Pydantic `AI_output`).
- `Runner.run(agent, input, max_turns=300)` — executor assíncrono que envia prompts ao modelo, gerencia turnos/conversas e retorna `result` com `final_output`.
- `AI_output` — modelo Pydantic que define o contrato de saída com campos `title` e `pr_content`.
- `PrGen(...)` — função `async` pública que orquestra:
  - validação de tamanho de entrada;
  - chunking quando necessário;
  - execução de agentes por chunk;
  - consolidação via agente de resumo (`prompt_system_summary`).
- `split_chunks(content, max_size)` — utilitário para dividir diffs por tamanho em bytes (preservando linhas).

O código também faz logging via `logger = logging.getLogger("PrGen_logger")`.


## 3. Dependências e variáveis de ambiente

### Dependências (visíveis no código):
- `agents` (módulo local com Agent, Runner, etc.)
- `pydantic.BaseModel` (para `AI_output`)
- `openai` (tipos importados, usado indiretamente pelo runner)
- `requests` (usado em outros modules; não diretamente em PrGen)
- `logging`, `os`, `asyncio`

### Variáveis de ambiente relevantes:
- `OPENAI_API_KEY` — chave da OpenAI usada pelo `Runner`/client. **Obrigatória** quando se chama `PrGen`.


## 4. Tipos e contratos (entrada/saída)

### Assinatura pública
```py
async def PrGen(
    OPENAI_API_KEY,
    user_id,
    content_pr: str = "diff dos arquivos mudados",
    model: str = "gpt-4.1-nano",
    MAX_INPUT_SIZE = 40000
) -> tuple[str, str]:
    # retorna (title, pr_content)
```

- `OPENAI_API_KEY` (str): chave da OpenAI — é definida em `os.environ['OPENAI_API_KEY']` dentro da função.
- `user_id` (qualquer): identificador do usuário responsável — propagado para logs/agents.
- `content_pr` (str): diff completo do PR.
- `model` (str): nome do modelo LLM a ser usado.
- `MAX_INPUT_SIZE` (int): limite em bytes para chunking (valor padrão 40000 bytes).

### Tipo de retorno
- Retorna uma tupla `(title, pr_content)` onde ambos são `str`.
- Internamente o `Runner` retorna um objeto `result` e `result.final_output` tem o modelo `AI_output` (fields: `title`, `pr_content`).


## 5. Fluxo de execução detalhado

1. **Seta variável de ambiente** `OPENAI_API_KEY` com o valor passado (a função sobrescreve `os.environ`).
2. **Calcula tamanho do input** em bytes e registra (`logger.info`).
3. **Se `input_size` > `MAX_INPUT_SIZE`**:
   - Chama `split_chunks(content_pr, MAX_INPUT_SIZE)` para obter lista de chunks (preservando linhas).
   - Para cada chunk: cria um `Agent` com `prompt_system_` e faz `await Runner.run(agent_, chunk, max_turns=300)`.
   - Coleta `title` e `pr_content` de cada `result.final_output` e concatena em `final_titles` e `final_pr`.
   - Cria um agente de sumarização (`prompt_system_summary`) e executa `Runner.run` para consolidar os chunks em um único título e PR final.
   - Retorna `(title_, final_pr_)` obtidos do agent de resumo.
4. **Se não ultrapassa limite**:
   - Cria um único `Agent` com `prompt_system_` e executa `Runner.run(agent, content_pr, max_turns=300)`.
   - Extrai `title` e `pr_content_` de `result.final_output` e retorna.

Observações:
- `max_turns=300` é um limite alto de interações/turnos interno do Runner.
- O processo é inteiramente assíncrono — `PrGen` é `async`.


## 6. Prompting: templates e diretrizes

Dois prompts principais:

### `prompt_system_` (prompt principal)
- Define o papel do sistema: especialista em criar descrições de PR e mensagens de commit.
- Determina estrutura desejada do corpo do PR (Descrição, Mudanças Principais, Por que, Como testar, Observações).
- Orienta a priorização (resumo e agrupamento de mudanças) e pede para **ignorar prompts de outros agentes** caso estejam presentes no diff.
- Instruções de formato do título e corpo e como lidar com diffs longos.

### `prompt_system_summary` (prompt de consolidação)
- Recebe títulos e resumos de chunks e deve consolidar em um PR final coerente.
- Regras de consolidação (evitar duplicação, agrupar, gerar título único).

**Boas práticas para prompts** (recomendado):
- Manter prompts curtos quando possível; usar instruções claras e exemplos.
- Inserir controle de formato de saída (ex.: JSON ou delimitadores) para parsing confiável.
- Considerar instruções para truncamento de conteúdo sensível ou binário.


## 7. Chunking / divisão de input

Função: `split_chunks(content: str, max_size: int)`
- Divide o texto em blocos por *linhas* (preserva quebras) até atingir `max_size` em bytes.
- Retorna lista de strings, cada uma com tamanho <= `max_size` (em bytes).

**Limitações**:
- Usa contagem de bytes simples; não há sobreposição/slide entre chunks (o que pode perder contexto nas fronteiras).
- Não faz algoritmos semânticos (ex.: dividir por função, arquivo ou módulo). Isso pode levar a cortes no meio de uma alteração lógica.

**Melhorias sugeridas**:
- Fazer chunking por arquivo (se o diff puder ser separado por `--- filename`), ou por bloco lógico (hunks do diff) para preservar contexto.
- Incluir overlap entre chunks (por exemplo 10% de linhas repetidas entre chunks) para evitar perda de contexto.


## 8. Integração com Runner/Agents

O código pressupõe a existência de um framework local `agents` com as APIs:
- `Agent(name, instructions, model, output_type=AI_output)` — define o agente.
- `Runner.run(agent, input_text, max_turns)` — executa e retorna `result` com estrutura `result.final_output`.

**Pontos de atenção**:
- O `Runner` deve aceitar agentes que retornem instâncias de `AI_output` ou um payload JSON que possa ser validado por Pydantic.
- O `Runner` e o agente LLM devem respeitar timeouts, handling de quotas e eventuais streaming de tokens.


## 9. Tratamento de erros, logs e observabilidade

Atualmente o código realiza *logging* informativo sobre tamanho do input e RAW OUTPUT. Recomenda-se:

- **Adicionar try/except** ao redor das chamadas ao `Runner.run` para capturar exceções (timeout, quota, parse errors) e retornar um erro controlado ou fallback.
- **Instrumentação**: registrar métricas como `tokens_in`, `tokens_out`, `latency`, `chunks_count`, `success/failure` por `user_id`.
- **Audit logs**: salvar um registro por PR processado com título gerado, tamanho do input e id do usuário (no MongoDB já existe infraestrutura de logs no projeto).
- **Tracing distribuído**: suportar `trace_id` em chamadas assíncronas para correlacionar logs (ex.: OpenTelemetry).


## 10. Segurança e privacidade

- **OPENAI_API_KEY** não deve ser logado nem exposto nos retornos.
- **Sanitização**: remover do diff strings sensíveis (chaves, tokens) antes de enviar ao modelo. Caso o diff contenha segredos, preferir bloquear a geração ou lançar alerta.
- **Consentimento**: se usuários subirem diffs contendo código de terceiros, checar contratos/licenças.
- **Validação de tamanho**: evitar que usuários maliciosos enviem payloads gigantescos que causem custo indevido.


## 11. Custos estimados e uso de tokens

- O código informa preços do modelo `gpt-4.1-nano` (exemplo): Input $0.10 por 1M tokens, Output $0.40 por 1M tokens — manter atenção às unidades e confirmar valores com provedor.
- Recomenda-se instrumentar contagem de tokens (antes e depois) para estimar custo por PR.
- Para reduzir custos: truncar diffs irrelevantes, sumarizar prévia- mente, ou usar um modelo mais barato para chunks e um modelo maior apenas para sumarização final.


## 12. Testes e estratégias de validação

**Unitários**:
- Testar `split_chunks` com strings contendo linhas longas, multibyte (UTF-8) e limites exatos.
- Mockar `Runner.run` para verificar composição de chunks e a chamada ao agent de resumo.
- Testar validação Pydantic `AI_output` frente a saídas inválidas do runner.

**Integração**:
- Testar fim-a-fim com um mock local do provedor LLM (simulando delays e limites).
- Testar com diffs reais pequenos e grandes (ex.: 10 arquivos vs 100 arquivos).

**QA**:
- Conferir títulos e corpo gerados para coerência, repetição e ausência de prompts de agentes embutidos.


## 13. Limitações conhecidas e riscos

1. **Perda de contexto entre chunks**: divisão por bytes pode cortar blocos lógicos.
2. **Dependência do `Runner`**: comportamento crítico assume que o Runner sempre converte saída em `AI_output`.
3. **Riscos de segurança**: diffs que contêm segredos.
4. **Custo**: grandes diffs geram muitos tokens; sem controle há gasto significativo.
5. **Assincronismo/concorrência**: se integrado em threads ou em servidores ASGI, atenção ao event loop e chamadas síncronas internas.


## 14. Melhorias e próximos passos (prioridade sugerida)

1. **Melhor chunking**: por arquivo/hunk com overlap.
2. **Saída estruturada (JSON)**: forçar que o modelo retorne um JSON padronizado (ex.: `{"title":"...","pr_content":"..."}`) para parsing confiável.
3. **Retries exponenciais** para falhas temporárias de LLM ou rede.
4. **Contagem de tokens** e capping automático (cortar texto muito grande com aviso ao usuário).
5. **Sistema de filas** (Celery/RQ) para processamentos longos e retrys.
6. **Mecanismo de aprovação** humano antes de mesclar PRs autogerados.
7. **Escaneamento de segredos** automático no diff antes de enviar para IA.
8. **Instrumentação de métricas** (Prometheus/OpenTelemetry).


## 15. Exemplos de uso

> Observação: o `PrGen` é `async` — exemplo em Python async.

### Exemplo mínimo
```py
import asyncio
from agents_prgen import PrGen

async def main():
    title, body = await PrGen(
        OPENAI_API_KEY="sk-xxxx",
        user_id=1,
        content_pr=open('diff.txt').read(),
        model='gpt-4.1-nano',
        MAX_INPUT_SIZE=40000
    )
    print('TITLE:', title)
    print('BODY:', body)

asyncio.run(main())
```

### Teste unitário (pseudocódigo)
```py
from unittest.mock import AsyncMock

async def test_prgen_chunks(monkeypatch):
    mock_runner_res = SimpleNamespace(final_output=SimpleNamespace(title='T1', pr_content='C1'))
    monkeypatch.setattr(Runner, 'run', AsyncMock(return_value=mock_runner_res))

    title, body = await PrGen('key', 1, content_pr='\n'.join(['line']*10000), model='gpt-4.1-nano', MAX_INPUT_SIZE=100)
    assert title is not None
    assert 'Descrição' in body
```

---

### Observação final
Esta documentação foi escrita para ser a referência técnica completa do módulo `PrGen`. Se desejar posso:
- gerar **JSON Schema** para `AI_output` e para o prompt de saída;
- criar testes `pytest` prontos;
- implementar o **chunking por arquivo** com overlap e um wrapper para contagem de tokens;
- criar um **endpoint** HTTP wrapper (Flask/FastAPI) que exponha `PrGen` de forma segura com rate-limiting e fila.

Diga qual dessas opções você quer que eu gere em seguida.

