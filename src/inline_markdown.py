from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception("Invalid syntax - unmatched delimiter")
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
    current = [TextNode(text, TextType.TEXT)]
    current = split_nodes_delimiter(current, "**", TextType.BOLD)
    current = split_nodes_delimiter(current, "_", TextType.ITALIC)
    current = split_nodes_delimiter(current, "`", TextType.CODE)
    current = split_nodes_link(current)
    current = split_nodes_image(current)
    return current

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches