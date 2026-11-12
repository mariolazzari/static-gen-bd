# Static site generator by boot.dev

## Static site

### HTML

```sh
python3 -m http.server 8888
```

### Markdown

- [Guide](https://www.markdownguide.org/cheat-sheet/)
- [HTML](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements)

## Nodes

### Text nodes

We're going to need a way to represent all the different types of inline text. We're going to be parsing Markdown text, and outputting it to HTML, so we need an intermediate representation of the text in our code.

When I say "inline" I just mean text that is part of a larger block of text. For us, this includes:

- text (plain)
- **Bold text**
- _Italic text_
- `Code text`
- Links, in this format: [anchor text](url)
- Images, in this format: ![alt text](url)
