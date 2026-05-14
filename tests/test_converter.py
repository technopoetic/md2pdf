import pytest
from pathlib import Path

from md2pdf.converter import convert


@pytest.fixture
def sample_md(tmp_path: Path) -> Path:
    md = tmp_path / "test.md"
    md.write_text("# Hello\n\nThis is a **test**.\n\n- item 1\n- item 2\n")
    return md


@pytest.fixture
def sample_css(tmp_path: Path) -> Path:
    css = tmp_path / "custom.css"
    css.write_text("body { color: red; }")
    return css


class TestConvert:
    def test_produces_pdf(self, sample_md: Path) -> None:
        result = convert(sample_md)
        assert result.suffix == ".pdf"
        assert result.exists()
        content = result.read_bytes()
        assert content[:4] == b"%PDF"

    def test_custom_output_path(self, sample_md: Path, tmp_path: Path) -> None:
        output = tmp_path / "subdir" / "output.pdf"
        result = convert(sample_md, output)
        assert result == output
        assert result.exists()

    def test_custom_css(self, sample_md: Path, sample_css: Path) -> None:
        result = convert(sample_md, css_path=sample_css)
        assert result.exists()

    def test_missing_input_raises(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="Input file not found"):
            convert(tmp_path / "nope.md")

    def test_missing_css_raises(self, sample_md: Path, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError, match="CSS file not found"):
            convert(sample_md, css_path=tmp_path / "nope.css")

    def test_default_output_name(self, sample_md: Path) -> None:
        result = convert(sample_md)
        assert result.name == "test.pdf"
