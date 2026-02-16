"""Fetch web pages as markdown using Jina AI Reader API."""

import time
import requests
from pathlib import Path
from urllib.parse import urlparse
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

JINA_READER_BASE = "https://r.jina.ai/"

console = Console()


def url_to_filename(url: str, base_path: str = "") -> str:
    """Convert a URL path to a safe markdown filename."""
    path = urlparse(url).path
    if base_path:
        path = path.replace(base_path, "")
    filename = path.strip("/").replace("/", "_") or "index"
    return f"{filename}.md"


def fetch_as_markdown(url: str, jina_api_key: Optional[str] = None) -> Optional[str]:
    """Fetch a single URL as markdown via Jina Reader API."""
    reader_url = f"{JINA_READER_BASE}{url}"
    headers = {"Accept": "text/markdown"}
    if jina_api_key:
        headers["Authorization"] = f"Bearer {jina_api_key}"

    try:
        response = requests.get(reader_url, headers=headers, timeout=60)
        response.raise_for_status()
        return _extract_content(response.text)
    except requests.RequestException as e:
        console.print(f"  [red]Error: {e}[/red]")
        return None


def _extract_content(raw: str) -> str:
    """Extract markdown content from Jina's response."""
    marker = "Markdown Content:"
    idx = raw.find(marker)
    return raw[idx + len(marker) :].strip() if idx != -1 else raw


def scrape_urls(
    urls: list[str],
    output_dir: str,
    base_path: str = "",
    jina_api_key: Optional[str] = None,
    delay: float = 1.5,
    combine: bool = False,
    combine_filename: str = "combined.md",
) -> dict:
    """
    Fetch multiple URLs as markdown and save to output directory.

    Returns dict with success/fail counts and file paths.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    results = {"success": 0, "failed": 0, "files": []}
    combined_parts = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        console=console,
    ) as progress:
        task = progress.add_task("Fetching docs...", total=len(urls))

        for i, url in enumerate(urls):
            filename = url_to_filename(url, base_path)
            filepath = out / filename

            # Skip existing
            if filepath.exists() and filepath.stat().st_size > 100:
                progress.update(task, advance=1, description=f"[yellow]Skip: {filename}")
                results["success"] += 1
                results["files"].append(str(filepath))
                if combine:
                    combined_parts.append(filepath.read_text(encoding="utf-8"))
                continue

            progress.update(task, description=f"[cyan]{filename}")
            content = fetch_as_markdown(url, jina_api_key)

            if content:
                filepath.write_text(content, encoding="utf-8")
                results["success"] += 1
                results["files"].append(str(filepath))
                if combine:
                    combined_parts.append(content)
                progress.update(task, advance=1, description=f"[green]{filename} ({len(content)} chars)")
            else:
                results["failed"] += 1
                progress.update(task, advance=1, description=f"[red]{filename}")

            if i < len(urls) - 1:
                time.sleep(delay)

    if combine and combined_parts:
        combined_path = out / combine_filename
        combined_path.write_text("\n\n---\n\n".join(combined_parts), encoding="utf-8")
        console.print(f"\n[green]Combined: {combined_path}[/green]")

    console.print(f"\n[bold]Success: {results['success']}  Failed: {results['failed']}[/bold]")
    console.print(f"[bold]Output: {out.resolve()}[/bold]")
    return results

