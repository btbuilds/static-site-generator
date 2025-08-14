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
    split_blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in split_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            stripped_blocks.append(stripped_block)
    return stripped_blocks

def block_to_block_type(block):
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