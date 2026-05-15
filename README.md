# md2pdf

Convert markdown files to PDF via an all-in-process Python pipeline — no subprocess calls, no temp files.

## Install

```bash
uv tool install .
```

## Usage

```bash
md2pdf INPUT.md                          # output: INPUT.pdf
md2pdf INPUT.md -o OUTPUT.pdf            # custom output path
md2pdf INPUT.md --css custom.css         # custom stylesheet
md2pdf INPUT.md --open                   # open PDF after creation
```

## Default Style

Georgia serif, US letter size, 1-inch margins. Override with `--css`.

## Requirements

- Python >=3.11
- System libraries: pango, cairo (required by WeasyPrint)

## Development

```bash
uv run pytest            # run tests
uv run pytest tests/test_cli.py  # single test file
```
