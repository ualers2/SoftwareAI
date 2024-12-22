import re

def ignore_python_code(text: str, replacement: str = "[CODE ON THE BOARD]") -> str:
    padrão = r"```python\n[\s\S]*?```"
    texto_limpo = re.sub(padrão, replacement, text, flags=re.DOTALL)
    texto_limpo = re.sub(r'\n{3,}', '\n\n', texto_limpo)
    return texto_limpo.strip()


def format_message(message):
    patternbash = r"^\s*```bash\n([\s\S]*?)```"
    highlight_pattern = r'`(.*?)`'
    title_pattern = r'### (.+?):'
    title_pattern2 = r'(###\s.*)'
    numberbeforcepoint_pattern = r'(\d+\.)'
    list_pattern = r'(\s{3}-\s.*)'
    minititulo_pattern = r'\*\*(.*?)\*\*'
    list_with_phrase_pattern = r"(\d+\.\s?\*\*`.*?`(?:\*\*)?\s*):\s*(.*)"

    # # Substitui blocos de código por HTML estilizado
    # message = re.sub(
    #     code_pattern,
    #     lambda m: (
    #         '<div style="position: relative; background-color: #1E1E1E; color: #D4D4D4; padding: 12px; border-radius: 8px; '
    #         'border: 1px solid #3C3C3C; font-family: Consolas, \'Courier New\', monospace; font-size: 14px; overflow: auto;">'
    #         '<div style="position: absolute; top: 8px; right: 8px; background-color: #022740; '
    #         'color: #FFFFFF; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-size: 12px;">'
    #         f'<b>#Python Code With {len(m.group(1).splitlines())} Lines</b>'
    #         '</div>'
    #         '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #1E1E1E; color: #D4D4D4;">' +
    #         ''.join(
    #             f'{line}\n'
    #             for i, line in enumerate(m.group(1).splitlines())
    #         ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>") +
    #         '</pre>'
    #         '</div>'
    #     ),
    #     message,
    #     flags=re.DOTALL
    # )


    message = ignore_python_code(message)

    message = re.sub(
        list_with_phrase_pattern,
        lambda m: (
            f'<li style="background-color: #F7F7F7; color: #000000; padding: 8px 12px; '
            f'border-radius: 6px; margin: 6px 0;"><b>' + m.group(1).replace("\n", "").replace("**", "").replace(":", "-").strip() + '</b>:<span style="color: #3b302c;">' + m.group(2).replace("\n", "").strip() + '</span></li>'
        ),
        message
    )
    message = re.sub(
        highlight_pattern,
        lambda m: (
            f'<span style="background-color: #F7F7F7; color: #000000; padding: 2px 4px; '
            f'border-radius: 3px;"><b>{m.group(1)}</b></span>'
        ),
        message
    )
    message = re.sub(
        minititulo_pattern,
        lambda m: (
            f'<span style="background-color: #F7F7F7; color: #022740; padding: 2px 4px; '
            f'border-radius: 3px;"><b>{m.group(1)}</b></span>'
        ),
        message
    )
    message = re.sub(
        numberbeforcepoint_pattern,
        lambda m: (
            f'<span style="background-color: #F7F7F7; color: #243096; padding: 2px 4px; '
            f'border-radius: 3px;"><b>{m.group(1).replace(".", ")")}</b></span>'
        ),
        message
    )
    message = re.sub(
        list_pattern,
        lambda m: (
            f'<span style="color: #1a0e03; padding: 2px 4px; '
            f'border-radius: 3px;">     {m.group(1)}</span>'
        ),
        message
    )
    message = re.sub(
        title_pattern,
        lambda m: (
            f'<h3 style="background-color: #F7F7F7; color: #000000; margin: 5px 0; font-size: 1.2em;"><b>{m.group(1)}</b></h3>'
        ),
        message
    )
    message = re.sub(
        title_pattern2,
        lambda m: (
            f'<h3 style="background-color: #F7F7F7; color: #000000; margin: 5px 0; font-size: 1.2em;"><b>{m.group(1).replace("### ", "")}</b></h3>'
        ),
        message
    )
    message = re.sub( 
        patternbash, 
        lambda m: ( 
            '<pre style="margin: 0; padding: 0; white-space: pre-wrap; background-color: #F7F7F7; color: #0e0042;"><b>' +
            ''.join(
                f'{line}'
                for i, line in enumerate(m.group(1).splitlines())
            ).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "") +
            '</b></pre>'
            '</div>'
            ), message, flags=re.MULTILINE,
        )
    message = message.replace("\n", "<br>")
    return message







