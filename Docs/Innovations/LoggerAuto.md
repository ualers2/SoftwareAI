## 📖 Agente para criação de degub de codigo com cprint  
## **Agente para criação de degub de codigo com cprint ** 
- **14/01/2024**  
  - Conceito: Agente para criação de degub de codigo com cprint 
  - anotacoes: sem alterar nenhuuma logica do codigo

```bash

crie o log para o codigo sem alterar nem adicionar nenhuma logica a mais (Debug é a variavel que ativa o log , lang é a linguagem que pode ser en para ingles e pt para portugues) 
```

```python
if self.Logger:
    if self.lang == "eng":
        cprint(f'📖 Processing file: {nome_do_arquivo}', 'blue')
    else:
        cprint(f'📖 Processando arquivo: {nome_do_arquivo}', 'blue')

```