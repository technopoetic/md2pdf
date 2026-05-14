import pytest
from click.testing import CliRunner
from pathlib import Path

from md2pdf.cli import main


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def sample_md(tmp_path: Path) -> Path:
    md = tmp_path / "test.md"
    md.write_text("# Hello\n\nA test document.\n")
    return md


class TestCli:
    def test_basic_conversion(self, runner: CliRunner, sample_md: Path) -> None:
        result = runner.invoke(main, [str(sample_md)])
        assert result.exit_code == 0
        assert "Created:" in result.output
        pdf_path = sample_md.with_suffix(".pdf")
        assert pdf_path.exists()

    def test_custom_output(self, runner: CliRunner, sample_md: Path, tmp_path: Path) -> None:
        output = str(tmp_path / "custom.pdf")
        result = runner.invoke(main, [str(sample_md), "-o", output])
        assert result.exit_code == 0
        assert Path(output).exists()

    def test_missing_input(self, runner: CliRunner, tmp_path: Path) -> None:
        result = runner.invoke(main, [str(tmp_path / "nope.md")])
        assert result.exit_code != 0

    def test_custom_css(self, runner: CliRunner, sample_md: Path, tmp_path: Path) -> None:
        css = tmp_path / "custom.css"
        css.write_text("body { color: red; }")
        result = runner.invoke(main, [str(sample_md), "--css", str(css)])
        assert result.exit_code == 0
