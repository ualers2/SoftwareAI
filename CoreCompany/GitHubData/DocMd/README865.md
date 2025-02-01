# 📚 Documentação do Sistema de Transcrição de YouTube

## 🌟 1. Introdução
Este software incrível permite transformar áudio de vídeos do YouTube em documentos PDF! 🎥 ➡️ 📄

Utilizamos as seguintes tecnologias:
- 🎧 `whisper` para transcrição de áudio
- 📺 `pytube` para download dos vídeos
- 📑 `FPDF` para geração de PDFs

## 🛠️ 2. Instalação
Execute o seguinte comando para instalar todas as dependências necessárias:

```bash
pip install pytube pydub torch torchvision torchaudio fpdf
```

💡 **Dica:** Para instalar o `whisper`, use:
```bash
pip install git+https://github.com/openai/whisper.git
```

## 🚀 3. Como Usar
1. 🔗 Defina a URL do vídeo do YouTube na variável `youtube_url`
2. ▶️ Execute o script
3. ✨ Pronto! Seu PDF será salvo como `Transcricao_Tutorial_YouTube.pdf`

Para executar:
```bash
python script.py
```

## 📖 4. Referência da API

### 📑 Classe PDFGenerator
Responsável por criar seus PDFs lindos!

#### Métodos:
- 🎨 `__init__(self, title)`
  - Inicia um novo PDF com título personalizado
  
- ✍️ `add_text(self, text)`
  - Adiciona conteúdo ao seu PDF
  
- 💾 `save(self, filename)`
  - Salva o PDF no arquivo especificado

### 🎵 Funções de Áudio

- 📥 `download_audio(youtube_url: str)`
  - Baixa o áudio do YouTube
  - Retorna: caminho do arquivo de áudio
  
- 🎤 `transcribe_audio(audio_path: str)`
  - Converte áudio em texto usando IA
  - Retorna: texto transcrito

## 👥 5. Contribuição
Adoraríamos sua ajuda! 🤝
- 🔄 Faça um fork
- ⭐ Adicione suas melhorias
- 📤 Envie um PR

## 📜 6. Licença
Este projeto está sob a licença MIT. 
Veja o arquivo LICENSE para mais detalhes! ⚖️

---
💪 **Desenvolvido com muito ❤️ pela comunidade**
