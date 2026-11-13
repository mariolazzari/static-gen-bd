import unittest

from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\n   \n\n  "), [])

    def test_single_block(self):
        self.assertEqual(
            markdown_to_blocks("Just one paragraph"),
            ["Just one paragraph"],
        )

    def test_excessive_newlines_between_blocks(self):
        md = "First block\n\n\n\nSecond block\n\n\n\n\nThird block"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block", "Second block", "Third block"],
        )

    def test_leading_and_trailing_whitespace_is_stripped(self):
        md = "   \n\n  Hello  \n\n   World   \n\n  "
        self.assertEqual(markdown_to_blocks(md), ["Hello", "World"])

    def test_preserves_single_newlines_inside_block(self):
        md = "line one\nline two\nline three"
        self.assertEqual(
            markdown_to_blocks(md),
            ["line one\nline two\nline three"],
        )

    def test_example_from_prompt(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )


if __name__ == "__main__":
    unittest.main()
