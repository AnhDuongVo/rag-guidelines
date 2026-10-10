"""Command line: ask a question, get a cited answer and a verification report."""

from __future__ import annotations

import typer
from rich.console import Console

from .config import Settings
from .corpus import CORPUS
from .generate import answer as generate_answer
from .retrieve import Retriever
from .verify import check_answer, summary

app = typer.Typer(add_completion=False, help="RAG over clinical guidelines with citation verification.")
console = Console()


@app.command()
def ask(
    question: str,
    k: int = typer.Option(3, help="chunks to retrieve"),
    live: bool = typer.Option(False, help="use the configured LLM endpoint instead of offline extractive"),
):
    """Answer a question from the guideline corpus and verify every citation."""
    settings = Settings()
    if live:
        settings.offline = False
    hits = Retriever().search(question, k=k)
    if not hits:
        console.print("[yellow]No relevant guideline found.[/yellow]")
        raise typer.Exit()
    ans = generate_answer(question, hits, settings)
    console.print(f"\n[bold]Answer[/bold]\n{ans}\n")
    console.print("[bold]Retrieved[/bold]")
    for c, s in hits:
        console.print(f"  [cyan]{c.id}[/cyan] ({s:.2f}) {c.source}")
    console.print("\n[bold]Citation check[/bold]")
    checks = check_answer(ans)
    for ch in checks:
        mark = "[green]OK[/green]" if ch.supported else "[red]FLAG[/red]"
        console.print(f"  {mark} {ch.reason}: {ch.sentence}")
    s = summary(checks)
    console.print(
        f"\n{s['supported']}/{s['sentences']} sentences passed lexical/numerical screening; semantic review required."
    )


@app.command()
def corpus():
    """List the guideline sources in the bundled corpus."""
    for c in CORPUS:
        console.print(f"[cyan]{c.id}[/cyan]  {c.source}")


if __name__ == "__main__":
    app()
