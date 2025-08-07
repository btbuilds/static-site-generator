from enum import Enum
from typing import Optional
from htmlnode import LeafNode

class TextType(Enum):
    """Enum representing different types of inline text formatting."""
    TEXT = "text"      # Plain text with no formatting
    BOLD = "bold"      # Bold text (**text**)
    ITALIC = "italic"  # Italic text (_text_)
    CODE = "code"      # Inline code (`text`)
    LINK = "link"      # Hyperlinks [text](url)
    IMAGE = "image"    # Images ![alt text](url)

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: Optional[str] = None):
        """Initialize a TextNode.
    
        Args:
            text: The raw text content of the node
            text_type: An Enum for the type of formatting (bold, italic, etc.) - Usage: TextType.LINK, etc
            url: (Optional) The URL for links/images, defaults to None for other types
            
        Example:
            node = TextNode("Click me!", TextType.LINK, "https://example.com")
        """
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, None)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href":text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
    raise ValueError("Not a valid TextNode - no valid TextType")