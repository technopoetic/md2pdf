# md2pdf

CLI tool: `md2pdf INPUT.md [-o OUTPUT.pdf] [--css FILE.css] [--open]`. Converts markdown to PDF via markdown-it-py → HTML → WeasyPrint, all in-process (no subprocess calls).

## Commands

```bash
uv run pytest                    # run tests
uv run pytest tests/test_cli.py  # single test file
uv run md2pdf README.md          # run the CLI
uv tool install .                # install globally
```

## Architecture

- `src/md2pdf/converter.py` — core logic: `convert(md_path, output_path, css_path) -> Path`
- `src/md2pdf/cli.py` — Click CLI wrapper, calls `convert()`
- `src/md2pdf/default.css` — embedded default stylesheet (Georgia serif, letter size, 1in margins)

No subprocess calls to weasyprint CLI; uses WeasyPrint Python API directly.

## Dev notes

- `src/` layout with hatchling build backend
- Python >=3.11, managed with `uv`
- Dev deps in `[dependency-groups]` (not `[optional-dependencies]`)
- Design spec: `docs/specs/2026-05-13-md2pdf-design.md`
- WeasyPrint requires system libraries (pango, cairo); if tests fail with import errors, check those are installed
