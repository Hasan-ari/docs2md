"""CLI interface for docs2md."""

import os
import click
from urllib.parse import urlparse
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
@click.version_option()
def main():
    """docs2md - Convert documentation sites to markdown using Claude AI + Jina Reader."""
    pass


@main.command()
@click.argument("url")
@click.option("-o", "--output", default=None, help="Output directory (auto-generated if omitted)")
@click.option("-i", "--instruction", default="", help="Extra instruction for Claude (e.g. 'Only API reference pages')")
@click.option("--anthropic-key", envvar="ANTHROPIC_API_KEY", required=True, help="Anthropic API key (or ANTHROPIC_API_KEY env)")
@click.option("--jina-key", envvar="JINA_API_KEY", default=None, help="Jina API key (or JINA_API_KEY env)")
@click.option("--model", default="claude-sonnet-4-20250514", help="Claude model for link discovery")
@click.option("-d", "--delay", default=1.5, type=float, help="Delay between Jina requests (seconds)")
@click.option("--combine/--no-combine", default=False, help="Also create a single combined markdown file")
@click.option("--combine-name", default="combined.md", help="Filename for combined output")
@click.option("-y", "--yes", is_flag=True, help="Skip confirmation prompt")
def scrape(url, output, instruction, anthropic_key, jina_key, model, delay, combine, combine_name, yes):
    """
    Scrape a full documentation site to markdown files.

    Claude AI reads the page, discovers all doc links from the navigation,
    then Jina Reader converts each page to clean markdown.
    """
    from docs2md.discovery import discover_links
    from docs2md.scraper import scrape_urls

    # Step 1: Claude discovers links
    console.print(f"\n[bold cyan]Claude is reading the page and discovering links...[/bold cyan]")
    console.print(f"   URL: {url}")
    if instruction:
        console.print(f"   Instruction: {instruction}")
    console.print()

    urls = discover_links(url, anthropic_key, instruction, model)

    # Display discovered URLs
    table = Table(title=f"Found {len(urls)} pages", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("URL", style="cyan")
    for i, u in enumerate(urls, 1):
        table.add_row(str(i), u)
    console.print(table)

    if not urls:
        console.print("[red]No links found.[/red]")
        return

    # Confirm
    if not yes and not click.confirm(f"\nProceed to fetch {len(urls)} pages as markdown?", default=True):
        return

    # Auto output dir
    if output is None:
        parsed = urlparse(url)
        output = parsed.path.strip("/").replace("/", "_") or parsed.netloc.replace(".", "_")
        output += "_md"

    base_path = urlparse(url).path

    # Step 2: Jina fetches markdown
    console.print(f"\n[bold green]Fetching markdown via Jina Reader...[/bold green]\n")
    scrape_urls(urls, output, base_path, jina_key, delay, combine, combine_name)


@main.command()
@click.argument("url")
@click.option("-o", "--output", default="output.md", help="Output filename")
@click.option("--jina-key", envvar="JINA_API_KEY", default=None, help="Jina API key")
def single(url, output, jina_key):
    """
    Fetch a single page as markdown.

    Example: docs2md single https://storybook.js.org/blog/storybook-mcp-sneak-peek/
    """
    from docs2md.scraper import fetch_as_markdown
    from pathlib import Path

    console.print(f"[cyan]Fetching:[/cyan] {url}")
    content = fetch_as_markdown(url, jina_key)

    if content:
        Path(output).write_text(content, encoding="utf-8")
        console.print(f"[green]Saved to {output} ({len(content)} chars)[/green]")
    else:
        console.print("[red]Failed.[/red]")


if __name__ == "__main__":
    main()

