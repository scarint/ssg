from textnode import *
from htmlnode import *
from inline_markdown import *




def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    node.__repr__()


main()