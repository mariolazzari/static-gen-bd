def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        cleaned = block.strip()
        if cleaned:
            blocks.append(cleaned)
    return blocks
