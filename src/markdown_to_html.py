from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, text_node_to_html_node, TextType

def markdown_to_html_node(markdown):
    """Convert full markdown text into an HTML node tree.

    Splits the input markdown into blocks, maps each block to the
    appropriate HTML structure, and returns a parent <div> node
    containing all children.

    Args:
        markdown (str): The raw markdown document.

    Returns:
        ParentNode: A <div> node containing the converted HTML structure
        of the markdown.

    Example:
        markdown_to_html_node("# Title\\n\\nHello **world**")
        # => ParentNode("div", [ParentNode("h1", ...), ParentNode("p", ...)])
    """
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block) # Determine the type of block
        node = block_to_html_node(block, block_type)
        children_nodes.append(node)
    add_parent_div = ParentNode(tag="div", children=children_nodes)
    return add_parent_div


def block_to_html_node(block, block_type):
    """Convert a markdown block into its corresponding HTML node.

    Maps each block type (heading, code, quote, list, paragraph) to
    the correct HTML structure. Handles inline markdown by converting
    text segments to HTML child nodes.

    Args:
        block (str): A single block of markdown text.
        block_type (BlockType): The type of block (e.g., HEADING, QUOTE).

    Returns:
        ParentNode: The root HTML node for this block.

    Example:
        block_to_html_node("## Subtitle", BlockType.HEADING)
        # => ParentNode("h2", [LeafNode(None, "Subtitle")])
    """
    node = None
    if block_type == BlockType.HEADING:
        h_num = heading_number(block)
        index = int(h_num) + 1
        text = block[index:]
        node = ParentNode(tag=f"h{h_num}", children=text_to_children(text))
    elif block_type == BlockType.CODE:
        code = block[4:-3] # Skip "```\n" at start and "\n```" at end
        code_text_node = TextNode(text=code, text_type=TextType.TEXT)
        code_html_node = text_node_to_html_node(code_text_node)
        code_tags = ParentNode(tag="code", children=[code_html_node])
        node = ParentNode(tag="pre", children=[code_tags])
    elif block_type == BlockType.QUOTE:
        lines = block.split("\n")
        cleaned_lines = []
        for line in lines:
            cleaned_line = line
            if line.startswith(">"): # Remove ">" and then any leading space    
                cleaned_line = line[1:].lstrip(" ")
            cleaned_lines.append(cleaned_line)
        text = "\n".join(cleaned_lines)
        node = ParentNode(tag="blockquote", children=text_to_children(text))
    elif block_type == BlockType.ORDERED:
        lines = block.split("\n")
        list_items = []
        for line in lines:
            cleaned_line = line.split(". ", 1)[1]
            list_items.append(ParentNode(tag="li", children=text_to_children(cleaned_line)))
        node = ParentNode(tag="ol", children=list_items)
    elif block_type == BlockType.UNORDERED:
        lines = block.split("\n")
        list_items = []
        for line in lines:
            cleaned_line = line.split("- ", 1)[1]
            list_items.append(ParentNode(tag="li", children=text_to_children(cleaned_line)))
        node = ParentNode(tag="ul", children=list_items)
    elif block_type == BlockType.PARAGRAPH:
        lines = block.split("\n")
        paragraph_text = " ".join(lines)
        node = ParentNode(tag="p", children=text_to_children(paragraph_text))
    return node

def heading_number(block):
    """Determine the heading level from a markdown heading block.

    Args:
        block (str): A block of text starting with '#' characters.

    Returns:
        str: A string number "1" - "6" indicating the heading level.

    Example:
        heading_number("### Title")  # => "3"
    """
    if block.startswith("# "):
        return "1"
    elif block.startswith("## "):
        return "2"
    elif block.startswith("### "):
        return "3"
    elif block.startswith("#### "):
        return "4"
    elif block.startswith("##### "):
        return "5"
    return "6" # defaults to 6 if it doesn't match 1-5
    
def text_to_children(text):
    """Convert a string of markdown text into a list of HTML nodes.

    Splits the text into TextNodes with inline formatting (bold,
    italics, links, images, etc.), then converts them into HTML nodes.

    Args:
        text (str): The raw inline markdown text.

    Returns:
        list[LeafNode]: A list of HTML nodes representing the inline content.

    Example:
        text_to_children("Hello **world**")
        # => [LeafNode(None, "Hello "), LeafNode("b", "world")]
    """
    list_text_nodes = text_to_textnodes(text)
    children_nodes = []
    for node in list_text_nodes:
        html_node = text_node_to_html_node(node)
        children_nodes.append(html_node)
    return children_nodes