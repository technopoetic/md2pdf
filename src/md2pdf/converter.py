from pathlib import Path

from markdown_it import MarkdownIt
from weasyprint import HTML

_DEFAULT_CSS = Path(__file__).parent / "default.css"


def convert(md_path: str | Path, output_path: str | Path | None = None, css_path: str | Path | None = None) -> Path:
    md_path = Path(md_path)
    if not md_path.exists():
        raise FileNotFoundError(f"Input file not found: {md_path}")

    if output_path is None:
        output_path = md_path.with_suffix(".pdf")
    else:
        output_path = Path(output_path)

    output_path.parent.mkdir(parents=True, exist_ok=True)

    md_text = md_path.read_text(encoding="utf-8")
    html_body = MarkdownIt().render(md_text)

    css_file = Path(css_path) if css_path else _DEFAULT_CSS
    if not css_file.exists():
        raise FileNotFoundError(f"CSS file not found: {css_file}")
    css_text = css_file.read_text(encoding="utf-8")

    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{css_text}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    HTML(string=html_doc, base_url=str(md_path.parent.resolve())).write_pdf(str(output_path))
    return output_path
