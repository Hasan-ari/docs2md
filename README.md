# docs2md

Convert any documentation site to clean markdown files using **Claude AI** for intelligent link discovery and **Jina Reader** for markdown conversion.

## Why?

Scraping documentation sites usually requires writing custom CSS selectors for each site's navigation. `docs2md` uses Claude AI to *read and understand* the page — just like a human would — making it work on any documentation site without configuration.

## How it works

```
You (URL + instruction)
        |
        v
   Claude AI (web_fetch)
   "Read the sidebar, find all doc links"
        |
        v
   URL list discovered
        |
        v
   Jina Reader (r.jina.ai)
   Converts each page -> clean markdown
        |
        v
   markdown files saved
```

1. **You provide a URL** — the entry page of a documentation section
2. **Claude reads the page** — using the `web_fetch` tool, Claude fetches the HTML, understands the sidebar/navigation, and extracts all documentation links
3. **Jina converts to markdown** — each discovered page is fetched through [Jina Reader](https://r.jina.ai) and saved as clean markdown

## Quick Start

### 1. Clone and setup virtual environment

```bash
git clone https://github.com/Hasan-ari/docs2md.git
cd docs2md

# Option A: Using make (recommended)
make setup
source .venv/bin/activate

# Option B: Manual venv
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 2. Configure API keys

```bash
cp .env.example .env
# Edit .env with your actual keys

# Then load them:
export $(grep -v '^#' .env | xargs)
```

### 3. Run

```bash
docs2md scrape https://developers.figma.com/docs/figma-mcp-server/
```

## Usage

### Scrape an entire documentation site

```bash
# Basic
docs2md scrape https://developers.figma.com/docs/figma-mcp-server/

# With instruction to filter pages
docs2md scrape https://react.dev/reference/ -i "Only the React hooks pages"

# Custom output dir + combined file
docs2md scrape https://docs.expo.dev/eas/workflows/ -o expo_docs --combine

# Skip confirmation
docs2md scrape https://some-docs.dev/api/ -y
```

### Fetch a single page

```bash
docs2md single https://storybook.js.org/blog/storybook-mcp-sneak-peek/ -o storybook.md
```

## Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output directory (auto-generated if omitted) |
| `-i, --instruction` | Extra guidance for Claude |
| `--model` | Claude model (default: claude-sonnet-4) |
| `-d, --delay` | Delay between requests in seconds (default: 1.5) |
| `--combine` | Also create a single combined markdown file |
| `-y, --yes` | Skip confirmation prompt |
| `--anthropic-key` | Anthropic API key (or `ANTHROPIC_API_KEY` env) |
| `--jina-key` | Jina API key (or `JINA_API_KEY` env) |

## Development

```bash
make setup           # Create venv + install dev deps
source .venv/bin/activate
make help            # Show all commands
make lint            # Run ruff linter
make format          # Auto-format code
make typecheck       # Run mypy
make test            # Run tests
make clean           # Remove venv and caches
```

## Project Structure

```
docs2md/
|-- .env.example          # API key template
|-- Makefile              # Dev workflow commands
|-- pyproject.toml        # Modern Python packaging + tool config
|-- requirements.txt
|-- setup.py
|-- docs2md/
    |-- __init__.py
    |-- cli.py            # CLI commands (scrape, single)
    |-- discovery.py      # Claude AI link discovery via web_fetch
    |-- scraper.py        # Jina Reader markdown conversion
```

## Cost

- **Claude API**: ~$0.01-0.05 per link discovery call (one call per site)
- **Jina Reader**: Free tier (20 RPM), or use API key for higher limits
- **web_fetch**: No additional cost beyond token pricing

## License

MIT
