
# Course Description Generator

## Introdução
O **Course Description Generator** é uma ferramenta que permite transcrever videoaulas e extrair informações relevantes, como tópicos abordados, objetivos de aprendizado, requisitos do curso e duração. A aplicação utiliza a biblioteca [Whisper](https://github.com/openai/whisper) para reconhecimento de fala e oferece uma interface fácil de usar para educadores e desenvolvedores.

## Instalação
Para executar o projeto, você precisa instalar as dependências necessárias. Execute o seguinte comando:

```bash
pip install whisper
```

Certifique-se também de ter um ambiente de execução compatível com a biblioteca Whisper.

## Uso
1. **Configuração**: Modifique a variável `video_file_path` na parte inferior do código principal com o caminho do vídeo que deseja analisar.

2. **Execução**: Execute o script Python:

```bash
python course_description_generator.py
```

A descrição do curso gerada será exibida no console.

## Estrutura do Projeto
```
.
├── course_description_generator.py
└── requirements.txt
```

- **course_description_generator.py**: Contém a classe responsável por gerar a descrição do curso.
- **requirements.txt**: Lista de dependências do projeto (pode ser criada automaticamente com os pacotes instalados).

## Referência de API
- `CourseDescriptionGenerator(video_path: str)`: Inicializa o gerador com o caminho do arquivo de vídeo.
- `transcribe_audio()`: Transcreve o áudio do vídeo usando o modelo Whisper.
- `extract_information()`: Extrai informações relevantes do vídeo.
- `generate_course_description() -> dict`: Gera e retorna um dicionário com a descrição do curso.

## Contribuição
Contribuições são bem-vindas! Se você deseja contribuir:
1. Faça um fork do repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-feature`).
3. Faça suas alterações e faça commit (`git commit -m 'Add new feature'`).
4. Envie para o repositório (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

## Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.