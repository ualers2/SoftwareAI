
# Landing Page Generator

## Introdução
O **Landing Page Generator** é uma ferramenta que permite a criação de páginas de aterrissagem personalizadas em HTML a partir de uma descrição em formato JSON. O gerador interpreta a descrição fornecida, contendo título, subtítulos, parágrafos, imagens e botões de chamada para ação, e monta um arquivo HTML pronto para uso.

## Instalação
Este projeto não possui dependências externas além do Python padrão. Certifique-se de ter o Python instalado em sua máquina.

## Uso
1. **Descrição JSON**: Modifique a variável `description_json` no final do script, inserindo suas informações específicas sobre a página.

2. **Execução**: Execute o script Python:

   ```bash
   python landing_page_generator.py
   ```

   A página de aterrissagem será salva no arquivo `landing_page.html`.

## Estrutura do Projeto
```
.
├── landing_page_generator.py
└── requirements.txt
```
- **landing_page_generator.py**: Contém a lógica do gerador e a função principal.
- **requirements.txt**: (Opcional) Pode ser utilizado para listar dependências futuras, se necessário.

## Referência de API
- `LandingPageGenerator(description: str)`: Inicializa o gerador com a descrição da página em JSON.
- `analyze_description()`: Analisa a descrição e extrai elementos como título, subtítulos, parágrafos e botões.
- `generate_html() -> str`: Gera o código HTML baseado nas informações extraídas.
- `save_to_file(filename: str)`: Salva o conteúdo HTML gerado em um arquivo especificado.

## Contribuição
Contribuições são bem-vindas! Para contribuir com o projeto:
1. Faça um fork do repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-feature`).
3. Faça suas alterações e commit (`git commit -m 'Add new feature'`).
4. Envie para sua branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request no repositório original.

## Licença
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.