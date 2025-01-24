## 📖 Codigo Gerado Pelo Agente É Salvo Automaticamente
## **Salvo Automaticamente** 
- **03/01/2024**  
  - Conceito: ao inves de criar codigos manuais e repetitivos solicitando o agente para que crie os codigos como main.py e salvar via codigo depois da resposta podemos apenas solicitar o agente para que cria e salve os arquivos usando a function autosave que é chamada com 2 argumentos o codigo e o caminho o solicitante sequer precisa fornecer os 2 argumentos já que o proprio agente tem a estrutura de caminhos do projeto e salva no caminho certo

## **Salvo Automaticamente** 
- **14/01/2024**  
  - 100% Funcional: testado em mais de 5 agentes
  - Inferencia: para que autosave funcione basta fornecer a solicitacao de salvamento em formto txt no seu prompt para o agente e em seguida fornecer tambem o caminho
  ```bash
  - O arquivo deve ser salvo automaticamente no formato `.txt` com o nome baseado no conteúdo:  
  **D:\\Company Apps\\Projetos de codigo aberto\\Pdf Studio\\CoreApp\\Qprocess\\roadmap\\{self.Name}.txt**  
  ```

```bash
  softwareai\CoreApp\SoftwareAI\Functions\autosave_function.py
```
```python

#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

def autosave(code, path):
    """
    Save the provided Python code string to a file.

    Parameters:
    ----------
    code (str): The Python code to save.
    path (str): The name of the file where the code will be saved.

    Returns:
    -------
    None
    """
    with open(path, 'w', encoding="utf-8") as file:
        file.write(code)

    return True


```