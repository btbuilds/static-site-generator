from enum import Enum
import re

class BlockType(Enum):
    """Enum representing different types of block-level markdown formatting."""
    HEADING = "heading"      # Heading level 1–6 (#...######...) followed by a space (### Title)
    CODE = "code"            # Code block enclosed in triple backticks (```code```)
    QUOTE = "quote"          # Each line starts with ">" (optional space) (> Quote)
    UNORDERED = "unordered"  # Each line starts with "- " (- List item)
    ORDERED = "ordered"      # Each line starts with incrementing number + ". " (1. Item)
    PARAGRAPH = "paragraph"  # Any block not matching other types

def markdown_to_blocks(markdown):
    """Split a markdown string into a list of block-level elements.

    Separates content into blocks using double newlines as delimiters,
    trimming whitespace and discarding empty blocks.

    Args:
        markdown: The raw markdown string to process.

    Returns:
        list[str]: A list of non-empty, trimmed markdown blocks.

    Example:
        markdown = "# Heading\\n\\nParagraph text"
        blocks = markdown_to_blocks(markdown)
        # ["# Heading", "Paragraph text"]
    """
    split_blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            stripped_blocks.append(stripped_block)
    return stripped_blocks

def block_to_block_type(block):
    """Determine the block-level markdown type of a given block.

    Inspects the formatting of the first line (and subsequent lines when needed)
    to classify the block as a heading, code block, quote, list, or paragraph.
    Ordered lists must start at 1 and increment sequentially on each line.

    Args:
        block: A single markdown block string.

    Returns:
        BlockType: The detected block type.
    
    Example:
        block = "1. First\\n2. Second"
        block_type = block_to_block_type(block)
        # BlockType.ORDERED
    """
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED
    return BlockType.PARAGRAPH