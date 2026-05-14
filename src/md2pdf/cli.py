import subprocess
import sys
from pathlib import Path

import click

from .converter import convert


@click.command()
@click.argument("input", type=click.Path(exists=True, path_type=Path))
@click.option("-o", "--output", type=click.Path(), default=None, help="Output PDF path (default: same name as input with .pdf)")
@click.option("--css", type=click.Path(exists=True, path_type=Path), default=None, help="Custom CSS file")
@click.option("--open", "open_pdf", is_flag=True, default=False, help="Open PDF after creation")
def main(input: Path, output: str | None, css: Path | None, open_pdf: bool) -> None:
    try:
        result = convert(input, output, css)
    except FileNotFoundError as e:
        click.echo(str(e), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"Conversion error: {e}", err=True)
        sys.exit(1)

    click.echo(f"Created: {result}")

    if open_pdf:
        subprocess.run(["xdg-open", str(result)], check=False)
