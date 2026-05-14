# md2pdf Design

## Problem

Converting markdown files to PDF currently requires a 50-line script with no markdown parsing (it just wraps raw MD text in HTML), subprocess calls to weasyprint CLI, and temp file management. It works but is fragile, not reusable, and has no real CLI interface.

## Solution

A proper CLI tool, installable via `uv tool install`, that converts markdown to PDF using an all-in-process Python pipeline. No subprocess calls, no temp files.

## Architecture

Pipeline: MD file → markdown-it-py (parse to HTML) → inject CSS → WeasyPrint Python API (render PDF) → write to file

Three modules:
- `cli.py` — Click CLI entry point
- `converter.py` — MD→HTML→PDF conversion logic
- `default.css` — embedded default stylesheet

## CLI Interface

```
md2pdf INPUT.md [-o OUTPUT.pdf] [--css FILE.css] [--open]
```

- `INPUT.md` — required positional argument
- `-o / --output` — output PDF path, defaults to input name with `.pdf` extension
- `--css` — custom CSS file, overrides embedded default
- `--open` — open PDF after creation via `xdg-open`
- Success prints `Created: output.pdf` to stdout
- Errors to stderr, exit code 1

## Default CSS

Carried from the existing script: Georgia serif, 8.5in max-width, 1in margins, 11pt body, clean heading hierarchy with h2 border-bottom. Embedded as a file in the package so the tool works with zero config.

## Error Handling

- Input file not found → clear error message, exit 1
- WeasyPrint rendering errors → caught, printed, exit 1
- Missing output directory → create it

## Dependencies

- `markdown-it-py` — markdown parsing
- `weasyprint` — HTML to PDF rendering
- `click` — CLI framework
- `pytest` — dev dependency for testing

## Project Structure

```
md2pdf/
  pyproject.toml
  src/
    md2pdf/
      __init__.py
      cli.py
      converter.py
      default.css
  tests/
    test_converter.py
    test_cli.py
```

## Install

`uv tool install ~/code/python/md2pdf` gives a global `md2pdf` command.

## Future (not in scope)

- Multiple themes/templates
- Front matter parsing
- Custom header/footer
- Table of contents generation
