import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """Classifica un singolo blocco di Markdown.

    Si assume che il blocco sia già stato passato per .strip()
    (vedi markdown_to_blocks).
    """
    lines = block.split("\n")

    # 1) Code block: apre con "```\n", chiude con "```".
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # 2) Heading: 1-6 '#' seguiti da uno spazio.
    #    La regex \#{1,6} è ancorata a inizio stringa grazie a re.match.
    #    "#######" fallisce perché dopo le prime 6 '#' non trova uno spazio.
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # 3) Quote: ogni riga inizia con '>'. Lo spazio dopo non è richiesto.
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # 4) Unordered list: ogni riga inizia con "- " (trattino + spazio).
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # 5) Ordered list: ogni riga "N. " con N che parte da 1 e incrementa di 1.
    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST

    # 6) Fallback.
    return BlockType.PARAGRAPH


def _is_ordered_list(lines: list[str]) -> bool:
    for i, line in enumerate(lines, start=1):
        m = re.match(r"^(\d+)\. ", line)
        if not m or int(m.group(1)) != i:
            return False
    return True
