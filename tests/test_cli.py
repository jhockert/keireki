from pathlib import Path

from typer.testing import CliRunner

from keireki.cli import app


def test_generate_cli(tmp_path: Path) -> None:
    runner = CliRunner()
    fixture = Path(__file__).parent / "fixtures" / "valid_profile.yaml"
    result = runner.invoke(
        app,
        ["generate", str(fixture), "--output-dir", str(tmp_path), "--debug-html"],
    )
    assert result.exit_code == 0, result.output
    assert (tmp_path / "rirekisho.pdf").stat().st_size > 0
    assert (tmp_path / "shokumukeirekisho.pdf").stat().st_size > 0
    assert (tmp_path / "rirekisho.html").stat().st_size > 0
    assert (tmp_path / "shokumukeirekisho.html").stat().st_size > 0
    shokumukeirekisho_html = (tmp_path / "shokumukeirekisho.html").read_text(
        encoding="utf-8"
    )
    assert "障害対応履歴を整理し、類似問い合わせの対応時間を短縮" in shokumukeirekisho_html
