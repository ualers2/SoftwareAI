# test_notion_refatorado.py
import os
import re
import logging
from dotenv import load_dotenv
from notion_client import Client
from notion_client.errors import APIResponseError

# --- config / logger (mantém logger se já existir) ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- carregar env e definir variáveis ---
os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv('Keys/keys.env')

NOTION_KEY = os.getenv("NOTION_KEY")
DATABASE_ID = "2885604fa64d806fa9d3e7535a1f47eb"  # seu database_id
TARGET_STATUS = "Pendente"  # valor desejado para filtrar (troque se preciso)

notion = Client(auth=NOTION_KEY)


def get_database_properties(db_id: str):
    """Retorna o objeto do database (properties) e ratifica tipos."""
    try:
        db = notion.databases.retrieve(db_id)
        return db
    except APIResponseError as e:
        logger.exception("Erro ao recuperar database: %s", e)
        raise


def list_status_options(db_id: str):
    """Lista os valores possíveis do campo Status (se existir)."""
    db = get_database_properties(db_id)
    props = db.get("properties", {})
    status_prop = props.get("Status")
    if not status_prop or status_prop.get("type") != "status":
        logger.warning("Propriedade 'Status' não encontrada ou não é do tipo 'status'. Tipos disponíveis: %s",
                       {k: v.get("type") for k, v in props.items()})
        return []
    options = status_prop.get("status", {}).get("options", [])
    valores = [opt["name"] for opt in options]
    logger.info("Valores possíveis para 'Status': %s", valores)
    return valores


def fetch_all_tasks(db_id: str, status_value: str = None):
    """Busca todas as páginas do database com paginação.
       Se status_value for None -> usa filtro is_not_empty (show all with status definido).
       Se status_value inválido -> usa is_not_empty e loga aviso.
    """
    # validar status
    valid_statuses = list_status_options(db_id)
    if status_value:
        if status_value not in valid_statuses:
            logger.warning("Status '%s' não encontrado entre as opções do DB. Usando is_not_empty em vez de equals.", status_value)
            status_filter = {"property": "Status", "status": {"is_not_empty": True}}
        else:
            status_filter = {"property": "Status", "status": {"equals": status_value}}
    else:
        status_filter = {"property": "Status", "status": {"is_not_empty": True}}

    results = []
    try:
        has_more = True
        start_cursor = None
        while has_more:
            query_kwargs = {
                "database_id": db_id,
                "filter": status_filter,
                "page_size": 100
            }
            if start_cursor:
                query_kwargs["start_cursor"] = start_cursor

            res = notion.databases.query(**query_kwargs)
            results.extend(res.get("results", []))
            has_more = res.get("has_more", False)
            start_cursor = res.get("next_cursor")
            logger.info("Página recebida: %d itens (has_more=%s)", len(res.get("results", [])), has_more)

        logger.info("Total de itens retornados: %d", len(results))
        return results

    except APIResponseError as e:
        logger.exception("Erro ao consultar database: %s", e)
        return []


def safe_get_title(properties: dict):
    """Retorna o título de forma segura. Usa chaves prováveis e faz fallback para id/url se vazio."""
    # chaves prováveis em PT/EN
    candidate_keys = ["Nome do projeto", "Nome", "Name", "title"]
    for key in candidate_keys:
        prop = properties.get(key)
        if prop and prop.get("type") in ("title",):
            title_list = prop.get("title", [])
            if title_list:
                return title_list[0].get("plain_text", "").strip()

    # fallback: tentar qualquer propriedade do tipo title
    for k, v in properties.items():
        if v.get("type") == "title":
            tl = v.get("title", [])
            if tl:
                return tl[0].get("plain_text", "").strip()

    # se tudo vazio, retorna vazio para caller tratar
    return ""


def get_rich_text_from_property(properties: dict, keys=None) -> str:
    """
    Retorna o texto contido numa propriedade do tipo rich_text.
    keys: lista de nomes possíveis da propriedade (ex: ["Descrição do projeto", "Descrição"])
    """
    if keys is None:
        keys = ["Descrição do projeto", "Descrição", "Description"]

    for key in keys:
        prop = properties.get(key)
        if not prop:
            continue
        # suporta tanto rich_text quanto title (fallback)
        if prop.get("type") == "rich_text":
            parts = prop.get("rich_text", [])
            texts = [seg.get("plain_text", "") for seg in parts if seg.get("plain_text")]
            return sanitize_text(" ".join(texts))
        if prop.get("type") == "title":
            parts = prop.get("title", [])
            texts = [seg.get("plain_text", "") for seg in parts if seg.get("plain_text")]
            return sanitize_text(" ".join(texts))
    return ""


def _extract_plain_from_rich_text_list(rich_list: list) -> str:
    """Helper: junta os plain_texts de uma lista rich_text."""
    if not rich_list:
        return ""
    return sanitize_text(" ".join([seg.get("plain_text", "") for seg in rich_list if seg.get("plain_text")]))

def sanitize_text(s: str) -> str:
    """Remove quebras de linha e colapsa múltiplos espaços."""
    if not s:
        return ""
    s = s.replace("\r", " ").replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def get_page_text_recursive(block_id: str) -> str:
    """
    Busca o conteúdo em blocos (children) de uma página (ou bloco) recursivamente.
    Retorna todo texto concatenado (parágrafos, headings, lists, callouts, quotes).
    """
    texts = []

    try:
        start_cursor = None
        while True:
            if start_cursor:
                res = notion.blocks.children.list(block_id=block_id, start_cursor=start_cursor, page_size=100)
            else:
                res = notion.blocks.children.list(block_id=block_id, page_size=100)

            for block in res.get("results", []):
                t = block.get("type")
                # tipos comuns com rich_text
                if t in ("paragraph", "heading_1", "heading_2", "heading_3",
                         "bulleted_list_item", "numbered_list_item",
                         "quote", "callout", "to_do"):
                    content = block.get(t, {})
                    rich = content.get("rich_text", []) or content.get("text", []) or []
                    texts.append(_extract_plain_from_rich_text_list(rich))

                # toggles, páginas aninhadas e lists podem ter children -> recursão
                if block.get("has_children"):
                    # chamar recursivamente e anexar
                    child_text = get_page_text_recursive(block["id"])
                    if child_text:
                        texts.append(child_text)

                # outros tipos (embed, image, video) -> opcionalmente podemos logar ou extrair captions
                if t in ("image", "video", "file"):
                    caption = block.get(t, {}).get("caption", [])
                    if caption:
                        texts.append(_extract_plain_from_rich_text_list(caption))

            if not res.get("has_more"):
                break
            start_cursor = res.get("next_cursor")

    except Exception as e:
        logger.exception("Erro ao ler blocks.children para %s: %s", block_id, e)

    return sanitize_text("\n".join([txt for txt in texts if txt]))


def extract_rich_segments_from_property(prop: dict):
    """
    Recebe a propriedade (ex: prop = properties['Descrição do projeto'])
    Retorna lista de segmentos: { 'text': str, 'href': str|None, 'annotations': {...}, 'type': 'text'|'mention'|'equation'}
    """
    segments = []
    if not prop:
        return segments

    # pode ser rich_text ou title
    key = 'rich_text' if prop.get('type') == 'rich_text' else ('title' if prop.get('type') == 'title' else None)
    if not key:
        return segments

    for seg in prop.get(key, []):
        # seg: objeto rich_text do Notion
        text = seg.get('plain_text', '') or ''
        href = None
        # o texto pode estar em seg['text'] com link
        if seg.get('href'):
            href = seg.get('href')
        elif seg.get('text') and seg['text'].get('link'):
            # formato alternativo dependendo do SDK
            link = seg['text'].get('link')
            if isinstance(link, dict):
                href = link.get('url')

        annotations = seg.get('annotations', {})
        rtype = seg.get('type')  # 'text', 'mention', 'equation'
        # para mentions podemos extrair info extra
        mention = seg.get('mention') if rtype == 'mention' else None

        segments.append({
            'text': text,
            'href': href,
            'annotations': annotations,
            'type': rtype,
            'mention': mention
        })
    return segments


def rich_segments_to_markdown(segments: list) -> str:
    """
    Converte uma lista de segmentos (do extract_rich_segments_from_property) para Markdown simples.
    Suporta bold, italic, strikethrough, code, links.
    """
    out = []
    for s in segments:
        txt = s.get('text', '')
        ann = s.get('annotations', {}) or {}
        # aplicar código primeiro (backticks)
        if ann.get('code'):
            txt = f'`{txt}`'
        # aplicar negrito / italic / strike / underline (underline não tem markdown direto)
        if ann.get('bold'):
            txt = f'**{txt}**'
        if ann.get('italic'):
            txt = f'*{txt}*'
        if ann.get('strikethrough'):
            txt = f'~~{txt}~~'
        # link
        href = s.get('href')
        if href:
            txt = f'[{txt}]({href})'
        out.append(txt)
    return ''.join(out)


# Versão que retorna segmentos ao invés de plain_text do seu get_page_text_recursive
def get_page_rich_segments_recursive(block_id: str) -> list:
    """
    Retorna lista de segmentos ricos (mantendo annotations/href) para todo o corpo da página (recursivo).
    Cada item desta lista é um dict: {'block_type': 'paragraph', 'segments': [ ... ] }
    """
    results = []
    try:
        start_cursor = None
        while True:
            if start_cursor:
                res = notion.blocks.children.list(block_id=block_id, start_cursor=start_cursor, page_size=100)
            else:
                res = notion.blocks.children.list(block_id=block_id, page_size=100)

            for block in res.get('results', []):
                t = block.get('type')
                container = block.get(t, {}) or {}
                segments = []

                # extrair rich_text dependendo do tipo de bloco
                if t in ("paragraph", "heading_1", "heading_2", "heading_3",
                         "bulleted_list_item", "numbered_list_item",
                         "quote", "callout", "to_do"):
                    # normalmente é container['rich_text']
                    rich_list = container.get('rich_text') or container.get('text') or []
                    for seg in rich_list:
                        segments.append({
                            'text': seg.get('plain_text', ''),
                            'href': seg.get('href') or (seg.get('text') and seg.get('text').get('link') and seg.get('text').get('link').get('url')),
                            'annotations': seg.get('annotations', {}),
                            'type': seg.get('type'),
                            'raw': seg
                        })

                # adicionar o bloco com seus segmentos (mesmo que vazio)
                results.append({
                    'block_id': block.get('id'),
                    'block_type': t,
                    'segments': segments
                })

                # recursão para children
                if block.get('has_children'):
                    child_segments = get_page_rich_segments_recursive(block['id'])
                    # anexar os filhos como itens separados (ou você pode concatenar)
                    if child_segments:
                        results.extend(child_segments)

            if not res.get('has_more'):
                break
            start_cursor = res.get('next_cursor')

    except Exception as e:
        logger.exception("Erro ao ler blocks.children para %s: %s", block_id, e)

    return results
def get_block_children(block_id: str) -> list:
    """
    Retorna a lista de blocos filhos imediatos de `block_id`.
    Cada item é o dict bruto do Notion para o bloco filho.
    Faz paginação automaticamente.
    """
    children = []
    try:
        start_cursor = None
        while True:
            if start_cursor:
                res = notion.blocks.children.list(block_id=block_id, start_cursor=start_cursor, page_size=100)
            else:
                res = notion.blocks.children.list(block_id=block_id, page_size=100)

            children.extend(res.get("results", []))

            if not res.get("has_more"):
                break
            start_cursor = res.get("next_cursor")

    except Exception as e:
        logger.exception("Erro ao recuperar filhos do bloco %s: %s", block_id, e)

    return children


def _make_block_node(block: dict) -> dict:
    """
    Normaliza um bloco bruto do Notion para uma estrutura simples:
    {id, type, plain_text (concat dos rich_text do bloco), raw}
    """
    t = block.get("type")
    container = block.get(t, {}) or {}
    # extrair texto plain do bloco quando aplicável
    rich = container.get("rich_text") or container.get("text") or []
    plain = _extract_plain_from_rich_text_list(rich)
    return {
        "id": block.get("id"),
        "type": t,
        "plain_text": plain,
        "has_children": block.get("has_children", False),
        "raw": block  # se quiser campos completos depois
    }


def get_block_tree(block_id: str, depth: int | None = None) -> dict:
    """
    Constrói uma árvore com o bloco raiz e seus filhos recursivamente.
    - block_id: id do bloco/página a partir do qual extrair
    - depth: profundidade máxima (None = sem limite). depth=0 retorna apenas o nó raiz.
    Retorna um dict: {'node': <node>, 'children': [ ... ]}
    """
    try:
        # recuperar o bloco raiz (para pegar tipo/conteúdo do próprio bloco)
        root = notion.blocks.retrieve(block_id=block_id)
    except Exception as e:
        logger.exception("Erro ao recuperar bloco raiz %s: %s", block_id, e)
        return {"node": None, "children": []}

    node = _make_block_node(root)

    if depth is not None and depth <= 0:
        return {"node": node, "children": []}

    # buscar filhos imediatos
    raw_children = get_block_children(block_id)
    children_nodes = []
    for child in raw_children:
        child_node = _make_block_node(child)
        # se tiver filhos e ainda permitimos profundidade, fazer recursão
        if child_node["has_children"]:
            # calcular nova profundidade
            next_depth = None if depth is None else (depth - 1)
            # recursão
            subtree = get_block_tree(child_node["id"], depth=next_depth)
            # substituir raw children pela árvore retornada
            children_nodes.append({"node": child_node, "children": subtree["children"]})
        else:
            children_nodes.append({"node": child_node, "children": []})

    return {"node": node, "children": children_nodes}

def retrieve_page(page_id: str, filter_properties: list | None = None) -> dict:
    """
    Recupera uma página via notion.pages.retrieve.
    - page_id: id da página (UUID do page retornado pela query do database)
    - filter_properties: lista de property ids se quiser limitar (opcional)
    Retorna o dict bruto da Notion (page).
    """
    try:
        if filter_properties:
            # A SDK do notion-client aceita parametros por nome; montar kwargs se necessário
            res = notion.pages.retrieve(page_id=page_id, filter_properties=filter_properties)
        else:
            res = notion.pages.retrieve(page_id=page_id)
        logger.info("Página recuperada: id=%s", res.get("id"))
        return res
    except Exception as e:
        logger.exception("Erro ao recuperar página %s: %s", page_id, e)
        return {}


def retrieve_page_with_children(page_id: str, depth: int | None = None) -> dict:
    """
    Recupera a página + árvore de blocos filhos (recursivo).
    - page_id: id da página
    - depth: profundidade de recursão (None = sem limite)
    Retorna { 'page': <page_obj>, 'blocks_tree': <tree> }.
    """
    page = retrieve_page(page_id)
    if not page:
        return {"page": None, "blocks_tree": None}

    # construir a árvore do corpo da página (raiz = page_id)
    tree = get_block_tree(page_id, depth=depth)
    logger.info("Árvore construída para página %s (children=%d)", page_id, len(tree.get("children", [])) if tree else 0)
    return {"page": page, "blocks_tree": tree}


def main():
    logger.info("Iniciando busca de tarefas no Notion (database_id=%s)", DATABASE_ID)

    # 1) mostrar opções de status (útil para confirmar ortografia)
    list_status_options(DATABASE_ID)

    # 2) buscar tarefas (filtra por TARGET_STATUS se válido, senão traz todos com status definido)
    tarefas = fetch_all_tasks(DATABASE_ID, TARGET_STATUS)

    if not tarefas:
        logger.info("Nenhuma tarefa retornada pela query.")
        return

    # 3) iterar e imprimir de forma segura
    for page in tarefas:
        props = page.get("properties", {})
        logger.info(f"props {props}")
        title = safe_get_title(props)
        status_name = None
        status_obj = props.get("Status", {}).get("status")
        if status_obj:
            status_name = status_obj.get("name")
        # se title está vazio, usar parte da url ou id como fallback
        if not title:
            title = page.get("url") or page.get("id")

        logger.info(f"title {title}")
        logger.info(f"status_name {status_name}")
        prop = props.get("Descrição do projeto")
        segments = extract_rich_segments_from_property(prop)
        md = rich_segments_to_markdown(segments)
        logger.info("Descrição (prop) MD: %s", md)

        page_id = page.get("id")
        if page_id:
            # 1) recuperar somente a página (metadados + propriedades)
            page_obj = retrieve_page(page_id)
            # imprimir propriedades resumidas
            props = page_obj.get("properties", {})
            logger.info("Página recuperada tem %d propriedades", len(props))

            # exemplo: pegar descrição (rich_text) direto do objeto page_obj
            desc_prop = props.get("Descrição do projeto") or props.get("Description") or props.get("Description")
            if desc_prop:
                segments = extract_rich_segments_from_property(desc_prop)
                logger.info("Descrição extraida da page.retrieve MD: %s", rich_segments_to_markdown(segments))

            # 2) recuperar a árvore de blocos (se quiser o corpo completo)
            page_with_children = retrieve_page_with_children(page_id, depth=None)
            blocks_tree = page_with_children.get("blocks_tree")
            if blocks_tree:
                # exemplo simples: printar primeira camada de filhos
                for child in blocks_tree.get("children", []):
                    node = child.get("node")
                    if node:
                        logger.info("child node: id=%s type=%s text_preview=%s", node['id'], node['type'], node['plain_text']['text_preview'])
        break
                
        # exemplo: se quiser atualizar o status programaticamente
        # page_id = page["id"]
        # notion.pages.update(page_id=page_id, properties={
        #     "Status": {"status": {"name": "Pendente"}}
        # })
        # logger.info("Atualizado status da página %s para 'Pendente'", page_id)

    logger.info("Fim.")


if __name__ == "__main__":
    main()
