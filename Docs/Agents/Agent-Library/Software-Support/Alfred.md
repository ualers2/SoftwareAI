## 📖 Sobre Alfred 
- **Descrição**
  - Alfred é o primeiro agente softwareai a entrar na força de trabalho da compania, o agente substitui a contratação de humanos para o suporte de duvidas e problemas dos usuarios , o agente pode ser inferido pelo usuario via `telegram` e `discord`

- **Plataform**  
  - ✅ Suporte em Tempo Real Via Telegram: Integração com telegram para inferencia ao agente por parte de usuarios
  - ✅ Suporte em Tempo Real Via Discord: Integração com Discord para inferencia ao agente por parte de usuarios

- **Caracteristicas**  
  - ✅ Recompensa por encontrar bugs: os usuarios sao insentivados mensalmente a reportar algum bug critico de segurança por exemplo o crakeamento do sistema de licensa e acessando em infinitas maquinas, caso o usuario reporte dependendo do nivel critico recebe entre 1 a 6 meses de licensa gratuita.
  - [] Destilação de Mensagens do usuario: Agent Destilation Integrado ao agente coletando e armazenando as conversas com o agente
  - ✅ Ticket de problema: usuario pode solicitar a criação de um ticket de problema, que será armazenado no banco de dados para resolucao do problema tecnico
  - [] Imagem relatando o problema: o usuario pode enviar uma imagem junto a uma descriçao informando o problema, que sera salvo no banco de dados e no bucket e informado ao Fundador ou/e Dono Da compania
  - ✅ Salva ticket com o problema 
  - ✅ Tempo médio de resolução: Tempo médio necessário para resolver um ticket desde sua abertura.
  - ✅ Pontuação de satisfação do cliente (CSAT): Classificação dada pelos clientes após o encerramento de um ticket.

- **Caracteristicas De Alta Prioridade**  
  - ✅ Alfred é capaz de moderar mensagens do chat usando omni e rastreamento de palavras 
  - ✅ apos alfred encontrar algo em risco potencial deleta a mensagem do alvo
  - ✅ se o alvo ainda continua enviando mensagens com palavras em risco potencial o alvo é banido do canal  
  - [] se o alvo for categorizado em risco potencial é automaticamente denunciado e bloqueado


- **Caracteristicas De Auto Melhoria**  
  - [] o usuario pode abrir um ticket de solicitacao de melhoria com email e uma descricao mais clara e detalhada possivel da melhoria desejada 
#
## 📖 Execução 

#### inicialização do agente em modo api
```bash
softwareai-cli select-agent-mode-api --name-agent "Alfred" --category-agent "Software_Support" --local-execute-port "101"
```
#
#### Requisição para inicialização do agente 
```python
import requests

url = "http://127.0.0.1:101/api/alfred_mode_api/NordVPN_Auto_Rotate"

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Resposta da API:", response.json())  # Se a API retornar JSON
    else:
        print(f"Erro: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Erro ao conectar à API: {e}")

```


# Apos os passos de execução 
- ✅ voce tera o agente em operação

