import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )

        result = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_split_italic(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT,
        )

        result = split_nodes_delimiter([node], "_", TextType.ITALIC)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_delimiters(self):
        node = TextNode(
            "This is `code` and `more code`",
            TextType.TEXT,
        )

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_delimiter_at_start(self):
        node = TextNode("`code` at start", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        node = TextNode("Ends with `code`", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_unclosed_delimiter(self):
        node = TextNode("This is `unclosed code", TextType.TEXT)

        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_node_unchanged(self):
        node = TextNode("Already bold", TextType.BOLD)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(result, [node])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("First `code`", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second `code`", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        expected = [
            TextNode("First ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("Already bold", TextType.BOLD),
            TextNode("Second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]

        self.assertEqual(result, expected)

    def test_empty_delimited_content(self):
        node = TextNode("Before `` after", TextType.TEXT)

        result = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("Before ", TextType.TEXT),
            TextNode(" after", TextType.TEXT),
        ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
