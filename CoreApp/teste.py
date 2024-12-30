
#########################################
# IMPORT SoftwareAI Libs 
from softwareai.CoreApp._init_libs_ import *
#########################################

init_agents_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "_init_agents_.py")
)

# Importação e inicialização
new_import = f"from softwareai.CoreApp.Agents.tet.teste import teste_1\n"
agent_initializer_entry = (
    f"        cls._agents['teste'] = teste_1()\n"
)

with open(init_agents_path, 'r+', encoding='utf-8') as file:
    content = file.read()

    # Adicionar a importação se não existir
    if new_import not in content:
        file.seek(0)
        file.write(new_import + content)
        file.truncate()
    else:
        print(f"Importação para já está presente.")

    # Adicionar a inicialização dentro do método `initialize_agents`
    if agent_initializer_entry not in content:
        # Localizar o início do método `initialize_agents`
        initialize_start = content.find("def initialize_agents(cls):")
        if initialize_start != -1:
            # Localizar onde termina as inicializações existentes
            insert_pos = content.find("cls._agents", initialize_start)
            end_of_initializations = content.find("\n", insert_pos) + 1

            # Inserir a inicialização no local correto
            updated_content = (
                content[:end_of_initializations]
                + agent_initializer_entry
                + content[end_of_initializations:]
            )
            file.seek(0)
            file.write(updated_content)
            file.truncate()

with open(init_agents_path, 'r+', encoding='utf-8') as file:
    content = file.read()
    if new_import not in content:
        file.seek(0)
        file.write(new_import + content)
        file.truncate()




















