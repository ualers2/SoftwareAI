
# Course Description Generator

## Introdução
O **Course Description Generator** é um software que analisa videoaulas para extrair informações importantes, como tópicos discutidos, objetivos de aprendizado, pré-requisitos e duração do curso. Ele utiliza a biblioteca OpenCV para manipulação de vídeos e pode ser facilmente integrado em projetos de educação online.

## Instalação
Para instalar as dependências necessárias, execute os seguintes comandos:

```bash
pip install opencv-python speechrecognition
```

## Uso
1. Modifique o caminho do arquivo de vídeo na linha 36 do script para o caminho do vídeo que deseja analisar.
2. Execute o script.

```bash
python course_description_generator.py
```

A descrição do curso será impressa na saída padrão.

## Referência de API
- `CourseDescriptionGenerator(video_path: str)`: Inicializa o gerador com o caminho do vídeo.
- `extract_info()`: Extrai informações do vídeo.
- `generate_course_description() -> Dict`: Gera e retorna um dicionário com a descrição do curso.

## Contribuição
Sinta-se à vontade para contribuir com o projeto:
- Fork o repositório
- Crie uma nova branch (`git checkout -b feature/nova-feature`)
- Faça suas alterações e commit (`git commit -m 'Add new feature'`)
- Envie para o repositório original (`git push origin feature/nova-feature`)
- Abra um Pull Request

## Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.