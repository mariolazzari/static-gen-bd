import unittest

from markdown import (
    extract_markdown_images,
    extract_markdown_links,
)


class TestMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_images(self):
        text = (
            "![rick roll](https://example.com/rick.gif) "
            "and ![obi wan](https://example.com/obi.jpeg)"
        )

        matches = extract_markdown_images(text)

        self.assertEqual(
            [
                ("rick roll", "https://example.com/rick.gif"),
                ("obi wan", "https://example.com/obi.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )

        self.assertEqual(
            [("link", "https://www.boot.dev")],
            matches,
        )

    def test_extract_multiple_links(self):
        text = "[boot dev](https://www.boot.dev) and [youtube](https://www.youtube.com)"

        matches = extract_markdown_links(text)

        self.assertEqual(
            [
                ("boot dev", "https://www.boot.dev"),
                ("youtube", "https://www.youtube.com"),
            ],
            matches,
        )

    def test_links_ignore_images(self):
        text = "![image](https://example.com/image.png) [link](https://example.com)"

        matches = extract_markdown_links(text)

        self.assertEqual(
            [("link", "https://example.com")],
            matches,
        )

    def test_images_ignore_links(self):
        text = "[link](https://example.com) ![image](https://example.com/image.png)"

        matches = extract_markdown_images(text)

        self.assertEqual(
            [("image", "https://example.com/image.png")],
            matches,
        )

    def test_no_matches(self):
        text = "This is just ordinary text."

        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_empty_text(self):
        self.assertEqual(extract_markdown_images(""), [])
        self.assertEqual(extract_markdown_links(""), [])


if __name__ == "__main__":
    unittest.main()
