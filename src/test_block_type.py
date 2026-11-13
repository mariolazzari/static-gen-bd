import unittest

from block_type import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    # ---------- Headings ----------
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_with_inline_formatting(self):
        self.assertEqual(
            block_to_block_type("## **Bold** and _italic_"),
            BlockType.HEADING,
        )

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Heading"), BlockType.PARAGRAPH)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # ---------- Code ----------
    def test_code_block_single_line(self):
        self.assertEqual(
            block_to_block_type("```\ncode here\n```"),
            BlockType.CODE,
        )

    def test_code_block_multiline(self):
        md = "```\ndef f():\n    return 1\n```"
        self.assertEqual(block_to_block_type(md), BlockType.CODE)

    def test_code_block_empty(self):
        self.assertEqual(block_to_block_type("```\n```"), BlockType.CODE)

    def test_code_block_missing_newline_after_open(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_code_block_missing_closing(self):
        self.assertEqual(block_to_block_type("```\ncode"), BlockType.PARAGRAPH)

    def test_code_block_missing_open_newline(self):
        self.assertEqual(block_to_block_type("code\n```"), BlockType.PARAGRAPH)

    def test_single_backtick_is_paragraph(self):
        self.assertEqual(block_to_block_type("`"), BlockType.PARAGRAPH)

    # ---------- Quote ----------
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> a quote"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(
            block_to_block_type("> line1\n> line2\n> line3"),
            BlockType.QUOTE,
        )

    def test_quote_no_space_after_gt(self):
        self.assertEqual(block_to_block_type(">quote"), BlockType.QUOTE)

    def test_quote_mixed_space(self):
        self.assertEqual(
            block_to_block_type("> line1\n>line2\n>"),
            BlockType.QUOTE,
        )

    def test_quote_with_one_line_not_quoted(self):
        self.assertEqual(
            block_to_block_type("> line1\nnot a quote"),
            BlockType.PARAGRAPH,
        )

    # ---------- Unordered list ----------
    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- a\n- b\n- c"),
            BlockType.UNORDERED_LIST,
        )

    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- a"), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("-a\n-b"), BlockType.PARAGRAPH)

    def test_unordered_list_mixed_is_paragraph(self):
        self.assertEqual(block_to_block_type("- a\n-b"), BlockType.PARAGRAPH)

    def test_unordered_list_with_inline(self):
        self.assertEqual(
            block_to_block_type("- **bold** item\n- `code` item"),
            BlockType.UNORDERED_LIST,
        )

    # ---------- Ordered list ----------
    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. a\n2. b\n3. c"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. a"), BlockType.ORDERED_LIST)

    def test_ordered_list_does_not_start_at_1(self):
        self.assertEqual(
            block_to_block_type("2. a\n3. b"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_skips_number(self):
        self.assertEqual(
            block_to_block_type("1. a\n3. b"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_does_not_increment(self):
        self.assertEqual(
            block_to_block_type("1. a\n1. b"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_double_digits(self):
        md = "\n".join(f"{i}. item" for i in range(1, 12))
        self.assertEqual(block_to_block_type(md), BlockType.ORDERED_LIST)

    def test_ordered_list_no_space_is_paragraph(self):
        self.assertEqual(
            block_to_block_type("1.a\n2.b"),
            BlockType.PARAGRAPH,
        )

    # ---------- Paragraph ----------
    def test_plain_paragraph(self):
        self.assertEqual(block_to_block_type("just some text"), BlockType.PARAGRAPH)

    def test_multiline_paragraph(self):
        self.assertEqual(
            block_to_block_type("line1\nline2\nline3"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_with_hash_mid_text(self):
        self.assertEqual(
            block_to_block_type("text with # in it"),
            BlockType.PARAGRAPH,
        )

    def test_paragraph_with_inline_formatting(self):
        self.assertEqual(
            block_to_block_type("This has **bold** and _italic_ words."),
            BlockType.PARAGRAPH,
        )


if __name__ == "__main__":
    unittest.main()
