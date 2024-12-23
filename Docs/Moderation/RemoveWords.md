#### 1. RemoveWords Algoritimich
Concept:
- the main concept of this algorithm is the recognition and censorship of certain words, initially it was tested in .srt subtitles

```python
filename = "teste1.srt"
with open(filename, "r", encoding="utf-8") as file:
    content = file.readlines()

from openai import OpenAI
client = OpenAI(api_key="")

model = "omni-moderation-latest"

for line in content:
    stripped_line = line.strip()
    timestamp_pattern = r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$'
    if re.match(timestamp_pattern, stripped_line):
        pass
    else:
        if stripped_line.isdigit():
            pass
        else:
            print(stripped_line)
            response = client.moderations.create(
                model=model,
                input=F"{stripped_line}",
            )
            flagged_value = response.results[0].flagged
            if flagged_value:
                words = stripped_line.split()
                for word in words:
                    response = client.moderations.create(
                        model=model,
                        input=F"{word}",
                    )
                    flagged_value = response.results[0].flagged
                    if flagged_value:
                        palavra_detectada = word 
                        with open(filename, "r", encoding="utf-8") as file:
                            content = file.readlines()
                        updated_content = [line.replace(palavra_detectada, "...") for line in content]
                        with open(filename, "w", encoding="utf-8") as file:
                            file.writelines(updated_content)

                        print(f"A palavra '{palavra_detectada}' foi censurada")

```
- we had great results with omni, however, to make something scalable in terms of word recognition in audio in real time, we need our own gpu model, so we will train `Qwen de 0.5b` or another model 

- the algo has the Qwen base model of 0.5b 
- algo will have openAI super intelligence models as an option
- algo will have the option of openAI moderation models

#### 2. Creating Algorithm 
steps:
  - [] we will generate 50 artificial data samples with words and do the first finnetunning on the model 
  - [] We will create a single repository for the algo despite it being a subfunction of softwareAI and mediacutsstudio
  - [] we will generate 200 artificial data samples with words and do the second finnetunning on the model