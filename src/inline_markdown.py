import re
from pydoc import text

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            result.append(node)
            continue
        splitted_text = node.text.split(delimiter)

        if len(splitted_text) % 2 == 0:
            raise Exception("delimeter not found")
        for i in range(len(splitted_text)):
            if splitted_text[i] == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(splitted_text[i], TextType.PLAIN_TEXT))
            else:
                result.append(TextNode(splitted_text[i], text_type))
    return result


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            result.append(node)
            continue
        node_string_arr = extract_markdown_images(node.text)
        if len(node_string_arr) == 0:
            result.append(node)
            continue
        remaining = node.text
        for alt, url in node_string_arr:
            before, after = remaining.split(f"![{alt}]({url})", 1)
            if before:
                result.append(TextNode(before, TextType.PLAIN_TEXT))
            result.append(TextNode(alt, TextType.IMAGE, url))
            remaining = after
        if remaining:
            result.append(TextNode(remaining, TextType.PLAIN_TEXT))
    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            result.append(node)
            continue
        node_string_arr = extract_markdown_links(node.text)
        if len(node_string_arr) == 0:
            result.append(node)
            continue
        remaining = node.text
        for alt, url in node_string_arr:
            before, after = remaining.split(f"[{alt}]({url})", 1)
            if before:
                result.append(TextNode(before, TextType.PLAIN_TEXT))
            result.append(TextNode(alt, TextType.LINK, url))
            remaining = after
        if remaining:
            result.append(TextNode(remaining, TextType.PLAIN_TEXT))
    return result


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
