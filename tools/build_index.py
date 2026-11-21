"""Build index.html (a standalone page for GitHub Pages) from whisker-meadow.html.

whisker-meadow.html is authored as an artifact body (no doctype/head skeleton),
so this wraps it with the doctype and viewport tag a plain browser needs.
"""
import pathlib

root = pathlib.Path(__file__).resolve().parent.parent
body = (root / "whisker-meadow.html").read_text(encoding="utf-8")
if body.startswith('<meta charset="utf-8">'):
    body = body[len('<meta charset="utf-8">'):].lstrip("\n")
page = (
    '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    + body + "\n</html>\n"
)
(root / "index.html").write_text(page, encoding="utf-8")
print("index.html written")
