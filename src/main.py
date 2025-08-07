from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev/")
    print(node)

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

main()