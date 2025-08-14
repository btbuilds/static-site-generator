from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    """Split text nodes on a specific inline formatting delimiter.

    Breaks TextNode instances of type TEXT into smaller nodes based on
    a given markdown delimiter (e.g., "**" for bold, "_" for italic, "`" for code).
    Delimiter sections alternate between plain text and the given text_type.
    Raises an exception if delimiters are unmatched.

    Args:
        old_nodes: List of TextNode objects to process.
        delimiter: The markdown delimiter to split on.
        text_type: The TextType to assign to text between matching delimiters.

    Returns:
        list[TextNode]: A new list of nodes with formatting applied where matched.

    Raises:
        ValueError: If the number of delimiters in a text node is odd.

    Example:
        split_nodes_delimiter([TextNode("Hello **World**!", TextType.TEXT)], "**", TextType.BOLD)
        # => [TextNode("Hello ", TEXT), TextNode("World", BOLD), TextNode("!", TEXT)]
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise ValueError("Invalid syntax - unmatched delimiter")
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def split_nodes_image(old_nodes):
    """Split text nodes into text and image nodes from markdown image syntax.

    Converts markdown images of the form ![alt text](url) into IMAGE-type TextNodes,
    preserving surrounding plain text as separate TEXT-type nodes.

    Args:
        old_nodes: List of TextNode objects to process.

    Returns:
        list[TextNode]: A new list with IMAGE nodes replacing markdown image syntax.

    Raises:
        ValueError: If an image delimiter is unmatched.

    Example:
        split_nodes_image([TextNode("Look ![cat](cat.png)", TEXT)])
        # => [TextNode("Look ", TEXT), TextNode("cat", IMAGE, "cat.png")]
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)
            remaining_text = node.text
            for image in images:
                split = remaining_text.split(f"![{image[0]}]({image[1]})", 1)
                if len(split) != 2:
                    raise ValueError("Invalid syntax - unmatched delimiter")
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                remaining_text = split[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    """Split text nodes into text and link nodes from markdown link syntax.

    Converts markdown links of the form [text](url) into LINK-type TextNodes,
    preserving surrounding plain text as separate TEXT-type nodes.

    Args:
        old_nodes: List of TextNode objects to process.

    Returns:
        list[TextNode]: A new list with LINK nodes replacing markdown link syntax.

    Raises:
        ValueError: If a link delimiter is unmatched.

    Example:
        split_nodes_link([TextNode("Click [here](https://example.com)", TEXT)])
        # => [TextNode("Click ", TEXT), TextNode("here", LINK, "https://example.com")]
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)
            remaining_text = node.text
            for link in links:
                split = remaining_text.split(f"[{link[0]}]({link[1]})", 1)
                if len(split) != 2:
                    raise ValueError("Invalid syntax - unmatched delimiter")
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                remaining_text = split[1]
            if remaining_text != "":
                new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    """Convert a markdown string with inline formatting into a list of TextNodes.

    Parses a string for bold, italic, inline code, links, and images, returning
    a sequence of TextNodes representing each segment.

    Args:
        text: The raw markdown text to parse.

    Returns:
        list[TextNode]: The parsed inline elements as TextNodes.

    Example:
        text_to_textnodes("This is **bold** and [linked](url)")
        # => [TextNode("This is ", TEXT), TextNode("bold", BOLD), TextNode(" and ", TEXT),
        #     TextNode("linked", LINK, "url")]
    """
    current = [TextNode(text, TextType.TEXT)]
    current = split_nodes_delimiter(current, "**", TextType.BOLD)
    current = split_nodes_delimiter(current, "_", TextType.ITALIC)
    current = split_nodes_delimiter(current, "`", TextType.CODE)
    current = split_nodes_link(current)
    current = split_nodes_image(current)
    return current

def extract_markdown_images(text):
    """Extract markdown images from a string.

    Args:
        text: The raw markdown string to search.

    Returns:
        list[tuple[str, str]]: A list of (alt text, URL) tuples for each image.

    Example:
        extract_markdown_images("![alt](img.png)")
        # => [("alt", "img.png")]
    """
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    """Extract markdown links from a string.

    Skips image syntax by ensuring matches are not preceded by '!'.

    Args:
        text: The raw markdown string to search.

    Returns:
        list[tuple[str, str]]: A list of (link text, URL) tuples for each link.

    Example:
        extract_markdown_links("[title](https://example.com)")
        # => [("title", "https://example.com")]
    """
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches