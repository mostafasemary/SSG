import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_htmlnode(self):
        node = HTMLNode("a","this is a link",None, {
    "href": "https://www.google.com",
    "target": "_blank",
})
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank"')

    def test_props_none(self):
        node2 = HTMLNode("p", "this is a paragraph","img",None)
        self.assertEqual(node2.props_to_html(), "")

    def test_props_not_eq(self):
        node3 = HTMLNode("article","this is article tag","img",{"color":"red"})
        self.assertEqual(node3.props_to_html(), ' color="red"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")


def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

        


if __name__ == "__main__": 
    unittest.main()