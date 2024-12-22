# Documentation of Tools
Available Functions

## analyze_file
Analyzes the content of a text file.

### Parameters
- file_path (string, required): Full path including the file name to be analyzed.

{
    "type": "function",
    "function": {
        "name": "analyze_file",
        "description": "Analyzes a txt file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path with the file name"
                }
            },
            "required": [
                "file_path"
            ]
        }
    }
},


## update_readme_to_github

Updates the README.md file of a GitHub repository.

### Parameters
- file_path_readme_improvements (string, required): Path of the improved README file
- repo_name (string, required): Name of the GitHub repository
- token (string, required): GitHub authentication token for API access
{
    "type": "function",
    "function": {
        "name": "update_readme_to_github",
        "description": "Updates the repository README on GitHub",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path_readme_improvements": {
                    "type": "string",
                    "description": "Path of the improved README"
                },
                "repo_name": {
                    "type": "string",
                    "description": "Name of the GitHub repository"
                },
                "token": {
                    "type": "string",
                    "description": "GitHub authentication token to perform API operations."
                }
            },
            "required": [
                "file_path_readme_improvements",
                "repo_name",
                "token"
            ]
        }
    }
},


## save_TXT

Saves content to a text file with different write modes.

### Parameters
- string (string, required): Content to be saved in the file
- filexname (string, required): Name of the file
- letra (string, required): Write mode
  - 'w': Creates a new file or overwrites an existing one
  - 'x': Creates a new file, fails if already exists
  - 'a': Appends content to the end of the file
- path (string, required): Directory where the file will be saved
{
    "type": "function",
    "function": {
        "name": "save_TXT",
        "description": "Saves a txt file",
        "parameters": {
            "type": "object",
            "properties": {
                "string": {
                    "type": "string",
                    "description": "The content of the txt file"
                },
                "filexname": {
                    "type": "string",
                    "description": "The name of the txt file"
                },
                "letra": {
                    "type": "string",
                    "description": "Letter 'w' opens for writing truncating the file first, letter 'x' creates a new file and opens it for writing, letter 'a' opens for writing appending to the end of the file if it exists"
                },
                "path": {
                    "type": "string",
                    "description": "The path where the txt will be saved"
                }
            },
            "required": [
                "string",
                "filexname",
                "letra",
                "path"
            ]
        }
    }
},


## save_code

Saves code files in different languages.

### Parameters
- code_string (string, required): Code content
- name_script (string, required): File name
- file_type (string, required): File type
  - Accepted values: "html", "js", "css", "py"
- path (string, required): Directory where the file will be saved
{
    "type": "function",
    "function": {
        "name": "save_code",
        "description": "Saves 4 types of code html, js, css, py",
        "parameters": {
            "type": "object",
            "properties": {
                "code_string": {
                    "type": "string",
                    "description": "The content of the code"
                },
                "name_script": {
                    "type": "string",
                    "description": "The name of the code"
                },
                "file_type": {
                    "type": "string",
                    "description": "The file type being html, js, css or py"
                },
                "path": {
                    "type": "string",
                    "description": "The path where the code will be saved"
                }
            },
            "required": [
                "code_string",
                "name_script",
                "file_type",
                "path"
            ]
        }
    }
},


## execute_python_code

Executes a Python script.

### Parameters
- filename (string, required): Full path of the Python file to be executed
{
    "type": "function",
    "function": {
        "name": "execute_python_code",
        "description": "Executes py codes",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The path with the .py file name"
                }
            },
            "required": [
                "filename"
            ]
        }
    }
},


## get_current_datetime

Returns the current date and time in a standardized format.

### Return
- String in the format "YYYY-MM-DD HH:MM:SS"
{
    "type": "function",
    "function": {
        "name": "get_current_datetime",
        "description": "Returns the current date and time in the format YYYY-MM-DD HH:MM:SS.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
},


## create_github_repo_and_upload

Creates a new repository on GitHub and uploads initial documentation and code.

### Parameters
- repo_name (string, required): Name of the new repository
- repo_description (string, required): Description of the repository
- readme_file_path (string, required): Path of the README.md file
- code_file_paths (array of strings, required): List of paths to Python files
- token (string, required): GitHub authentication token
```
    {
        "type": "function",
        "function": {
            "name": "add_projectmap_to_github",
            "description": "Uploads the project files, including documentation, timeline, roadmap, and analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "Repository name on GitHub."
                    },
                    "timeline_file_path": {
                        "type": "string",
                        "description": "Path of the project's timeline file."
                    },
                    "spreadsheet_file_path": {
                        "type": "string",
                        "description": "Path of the project's spreadsheet file."
                    },
                    "pre_project_file_path": {
                        "type": "string",
                        "description": "Path of the pre-project file."
                    },
                    "Roadmap_file_path": {
                        "type": "string",
                        "description": "Path of the project's Roadmap file."
                    },
                    "analise_file_path": {
                        "type": "string",
                        "description": "Path of the project's analysis file."
                    },
                    "token": {
                        "type": "string",
                        "description": "GitHub authentication token to perform API operations."
                    }
                },
                "required": [
                    "repo_name",
                    "timeline_file_path",
                    "spreadsheet_file_path",
                    "pre_project_file_path",
                    "Roadmap_file_path",
                    "analise_file_path",
                    "token"
                ]
            }
        }
    },
```

## add_projectmap_to_github

Uploads project planning and analysis documents to a GitHub repository.

### Parameters
- repo_name (string, required): Name of the repository
- timeline_file_path (string, required): Path of the project timeline file
- spreadsheet_file_path (string, required): Path of the project spreadsheet
- pre_project_file_path (string, required): Path of the pre-project file
- Roadmap_file_path (string, required): Path of the project roadmap file
- analise_file_path (string, required): Path of the project analysis file
- token (string, required): GitHub authentication token


```
    {
        "type": "function",
        "function": {
            "name": "add_projectmap_to_github",
            "description": "Realiza o upload dos arquivos do projeto, incluindo documentação, timeline, roadmap e análises.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_name": {
                        "type": "string",
                        "description": "Nome do repositório no GitHub."
                    },
                    "timeline_file_path": {
                        "type": "string",
                        "description": "Caminho do arquivo de timeline do projeto."
                    },
                    "spreadsheet_file_path": {
                        "type": "string",
                        "description": "Caminho da planilha do projeto."
                    },
                    "pre_project_file_path": {
                        "type": "string",
                        "description": "Caminho do arquivo de pré-projeto."
                    },
                    "Roadmap_file_path": {
                        "type": "string",
                        "description": "Caminho do arquivo de Roadmap do projeto."
                    },
                    "analise_file_path": {
                        "type": "string",
                        "description": "Caminho do arquivo de análise do projeto."
                    },
                    "token": {
                        "type": "string",
                        "description": "Token de autenticação do GitHub para realizar operações na API."
                    }
                },
                "required": [
                    "repo_name",
                    "timeline_file_path",
                    "spreadsheet_file_path",
                    "pre_project_file_path",
                    "Roadmap_file_path",
                    "analise_file_path",
                    "token"
                ]
            }
        }
    }
```

## improve_code_and_create_pull_request

Implement code improvements and create a Pull Request on GitHub.

### Parameters
- `repo_owner` (string, required): Name of the repository owner
- `repo_name` (string, required): Repository name
- `branch_name` (string, required): Name of the branch for the changes
- `file_path` (string, required): Path of the file to be improved
- `commit_message` (string, required): Descriptive commit message
- `improvements` (string, required): Improved code
- `pr_title` (string, required): Pull Request title
- `token` (string, required): GitHub authentication token
```
    {
        "type": "function",
        "function": {
            "name": "improve_code_and_create_pull_request",
            "description": "Implements code improvements and creates a pull request on GitHub.",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_owner": {
                        "type": "string",
                        "description": "Repository owner's name on GitHub."
                    },
                    "repo_name": {
                        "type": "string",
                        "description": "Repository name on GitHub."
                    },
                    "branch_name": {
                        "type": "string",
                        "description": "Branch name where the code will be updated."
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path of the file in the repository."
                    },
                    "commit_message": {
                        "type": "string",
                        "description": "Commit message describing the improvements."
                    },
                    "improvements": {
                        "type": "string",
                        "description": "New improved code."
                    },
                    "pr_title": {
                        "type": "string",
                        "description": "Pull request title."
                    },
                    "token": {
                        "type": "string",
                        "description": "GitHub authentication token."
                    }
                },
                "required": [
                    "repo_owner",
                    "repo_name",
                    "branch_name",
                    "file_path",
                    "commit_message",
                    "improvements",
                    "pr_title",
                    "token"
                ]
            }
        }
    }

```