"""
Use Claude API with web_fetch to intelligently discover documentation links.
Claude reads the page, understands the navigation structure, and extracts all doc URLs.
"""

import json
import anthropic
from urllib.parse import urlparse
from rich.console import Console

console = Console()


def discover_links(
    base_url: str,
    anthropic_api_key: str,
    instruction: str = "",
    model: str = "claude-sonnet-4-20250514",
) -> list[str]:
    """
    Use Claude + web_fetch to discover all documentation page URLs.

    Claude fetches the page, reads the sidebar/navigation, and returns
    a structured list of all documentation URLs.
    """
    client = anthropic.Anthropic(api_key=anthropic_api_key)

    user_prompt = f"""I need you to extract all documentation page URLs from this site's navigation/sidebar:

URL: {base_url}

Please fetch this URL, then look at the page's navigation structure (sidebar, menu, table of contents, etc.) and extract ALL documentation page links that belong to this documentation section.

{f'Additional instruction: {instruction}' if instruction else ''}

Return your answer as a JSON array of full URLs, nothing else. Example format:
["https://example.com/docs/page1/", "https://example.com/docs/page2/"]

Important:
- Include the base URL itself in the list
- Only include pages that are part of this documentation section
- Return full absolute URLs
- Do NOT include external links, GitHub links, or unrelated pages
- Return ONLY the JSON array, no explanation"""

    response = client.beta.messages.create(
        model=model,
        max_tokens=4096,
        betas=["web-fetch-2025-09-10"],
        messages=[{"role": "user", "content": user_prompt}],
        tools=[
            {
                "type": "web_fetch_20250910",
                "name": "web_fetch",
                "max_uses": 3,
                "allowed_domains": [_extract_domain(base_url)],
            }
        ],
    )

    urls = _parse_url_list(response)

    if not urls:
        console.print("[yellow]Warning: Claude couldn't find links. Returning base URL only.[/yellow]")
        return [base_url]

    return urls


def _extract_domain(url: str) -> str:
    """Extract domain from URL for allowed_domains."""
    return urlparse(url).netloc


def _parse_url_list(response) -> list[str]:
    """Extract URL list from Claude's response content blocks."""
    for block in response.content:
        if hasattr(block, "text"):
            text = block.text.strip()
            start = text.find("[")
            end = text.rfind("]") + 1
            if start != -1 and end > start:
                try:
                    urls = json.loads(text[start:end])
                    if isinstance(urls, list) and all(isinstance(u, str) for u in urls):
                        return urls
                except json.JSONDecodeError:
                    continue
    return []
