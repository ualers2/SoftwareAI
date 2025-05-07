## 📤 Instrução: Criar repositório e fazer upload dos arquivos locais

### 🎯 Objetivo:
Criar um novo repositório GitHub para o projeto, listar os arquivos do projeto local e fazer o upload completo desses arquivos para o repositório recém-criado.

### 🔧 Etapas obrigatórias:

#### 1. Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo cronograma para que seja possivel a criacao do nome do projeto
autogetlocalfilecontent:
- preferred_name: "cronograma.md"
- fallback_names: ["cronograma.md"]
- search_dir: {doc_md}

---

#### 2. Criar o repositório com `autocreaterepo`
Use a ferramenta `autocreaterepo` para criar o repositório do projeto com os seguintes dados:
- `description`: uma breve descrição do projeto (máx. 250 caracteres).
- `repo_name`: o nome do projeto, em slug (sem espaços, sem acentos).
- `private`: true
- `githubtoken`: {githubtoken}
- `repo_owner`: {repo_owner}

---

#### 3. Listar os arquivos do projeto local com `autolistlocalproject`
Use a ferramenta `autolistlocalproject` para listar os caminhos dos arquivos do projeto.  
- path_project: {path_ProjectWeb}
> ⚠️ O conteúdo dos arquivos não precisa ser lido — apenas os **caminhos** são necessários.

---

#### 4. Fazer upload dos arquivos com `autoupload`
Com os caminhos obtidos na etapa anterior, use a ferramenta `autoupload` para enviar os arquivos ao repositório:
- `repo_name`: nome do repositório criado.
- `repo_owner`: {repo_owner}
- `softwarepypath`: lista de caminhos retornada pelo `autolistlocalproject`.
- `token`: {githubtoken}

---

