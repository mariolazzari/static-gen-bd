from block_type import BlockType, block_to_block_type
from htmlnode import HTMLNode
from markdown_blocks import markdown_to_blocks
from text_to_textnodes import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = [block_to_html_node(block) for block in blocks]
    return HTMLNode("div", None, children)


# ---------- dispatcher ----------
def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"invalid block type: {block_type}")


# ---------- helpers ----------
def text_to_children(text: str) -> list[HTMLNode]:
    """Applica il parser inline (bold/italic/code/link/image) e ritorna HTMLNode."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(t) for t in text_nodes]


def paragraph_to_html_node(block: str) -> HTMLNode:
    # Le righe di un paragrafo si uniscono con UNO spazio (a capo "soft" Markdown).
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return HTMLNode("p", None, text_to_children(paragraph))


def heading_to_html_node(block: str) -> HTMLNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level < 1 or level > 6 or level + 1 >= len(block):
        raise ValueError(f"invalid heading level {level} in block: {block!r}")
    # Salta gli '#' e lo spazio che li segue.
    text = block[level + 1 :]
    return HTMLNode(f"h{level}", None, text_to_children(text))


def code_to_html_node(block: str) -> HTMLNode:
    if not (block.startswith("```\n") and block.endswith("```")):
        raise ValueError("invalid code block")
    # Contenuto tra "```\n" (4 char) e la chiusura "```" (3 char).
    # Nota: block[4:-3] conserva il \n finale prima della chiusura,
    # cosa che il test si aspetta.
    raw_code = block[4:-3]
    text_node = TextNode(raw_code, TextType.TEXT)  # niente parsing inline
    code_node = HTMLNode("code", None, [text_node_to_html_node(text_node)])
    return HTMLNode("pre", None, [code_node])


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError(f"invalid quote line: {line!r}")
        # rimuove tutti i '>' iniziali + spazio opzionale
        cleaned.append(line.lstrip(">").strip())
    # Le righe di una quote si uniscono in un unico paragrafo inline.
    content = " ".join(cleaned)
    return HTMLNode("blockquote", None, text_to_children(content))


def unordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    children = []
    for item in items:
        if not item.startswith("- "):
            raise ValueError(f"invalid unordered list item: {item!r}")
        text = item[2:]
        children.append(HTMLNode("li", None, text_to_children(text)))
    return HTMLNode("ul", None, children)


def ordered_list_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    children = []
    for item in items:
        # split su ". " una sola volta: gestisce anche "10. item"
        num, sep, text = item.partition(". ")
        if not sep:
            raise ValueError(f"invalid ordered list item: {item!r}")
        children.append(HTMLNode("li", None, text_to_children(text)))
    return HTMLNode("ol", None, children)
