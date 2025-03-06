from enum import Enum
from textnode import *
from htmlnode import *
from inline_markdown import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def markdown_to_blocks(markdown):
    strings = markdown.strip().split("\n\n")
    blocks = []
    for i in range(0, len(strings)):
        if strings[i] == "":
            continue
        else:
            blocks.append(strings[i].strip())
    return blocks

def block_to_block_type(block):
    if block.startswith("#"):
        return BlockType.HEADING
    if block.startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        return BlockType.QUOTE
    if block.startswith("- "):
        return BlockType.ULIST
    if block[0].isdigit() and block[1] == ".":
        return BlockType.OLIST
    return BlockType.PARAGRAPH

# from boot.dev. A bit more thorough, in that it examines all the following lines
# def block_to_block_type(block):
#     lines = block.split("\n")

#     if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
#         return BlockType.HEADING
#     if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
#         return BlockType.CODE
#     if block.startswith(">"):
#         for line in lines:
#             if not line.startswith(">"):
#                 return BlockType.PARAGRAPH
#         return BlockType.QUOTE
#     if block.startswith("- "):
#         for line in lines:
#             if not line.startswith("- "):
#                 return BlockType.PARAGRAPH
#         return BlockType.ULIST
#     if block.startswith("1. "):
#         i = 1
#         for line in lines:
#             if not line.startswith(f"{i}. "):
#                 return BlockType.PARAGRAPH
#             i += 1
#         return BlockType.OLIST
#     return BlockType.PARAGRAPH


# def markdown_to_html(markdown):
#     blocks = markdown_to_blocks(markdown)
#     for block in blocks:
#         block_type = block_to_block_type(block)
#         match block_type:
#             case BlockType.PARAGRAPH:
#                 # convert block to text node
#                 text_node = TextNode(block, TextType.TEXT)
#                 # convert to html leaf node
#                 # tag p
#                 # value text
#                 # 
#             case BlockType.HEADING:
#                 text_node = TextNode(block, TextType.TEXT)
#             case BlockType.CODE:
#                 pass
#             case BlockType.QUOTE:
#                 pass
#             case BlockType.ULIST:
#                 pass
#             case BlockType.OLIST:
#                 pass


## From boot.dev. Ch4L3:
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)