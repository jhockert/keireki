from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel

from keireki.render import ProfileLoadError, load_profile, render_documents

app = typer.Typer(help="Generate Japanese resume PDFs from structured YAML.")
console = Console()


@app.callback()
def main() -> None:
    """Generate Japanese resume PDFs from structured YAML."""


@app.command()
def generate(
    profile_path: Annotated[Path, typer.Argument(help="Path to profile.yaml")],
    output_dir: Annotated[Path, typer.Option("--output-dir", "-o")] = Path("dist"),
    debug_html: Annotated[bool, typer.Option("--debug-html")] = False,
) -> None:
    """Generate 履歴書 and 職務経歴書 PDFs."""
    try:
        profile = load_profile(profile_path)
        console.print(f"Loaded {profile_path}")
        generated = render_documents(profile, output_dir=output_dir, debug_html=debug_html)
    except ProfileLoadError as exc:
        console.print(Panel(str(exc), title="Validation failed", style="red"))
        raise typer.Exit(code=1) from exc

    console.print(f"Validated profile with {len(generated.warnings)} warnings")
    for warning in generated.warnings:
        console.print(f"[yellow]Warning:[/] {warning}")
    console.print(f"Generated {generated.rirekisho_pdf}")
    console.print(f"Generated {generated.shokumukeirekisho_pdf}")


if __name__ == "__main__":
    app()
