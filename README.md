# docs2md

Convert any documentation site to clean markdown files using **Claude AI** for intelligent link discovery and **Jina Reader** for markdown conversion.

## Why?

Scraping documentation sites usually requires writing custom CSS selectors for each site's navigation. `docs2md` uses Claude AI to *read and understand* the page — just like a human would — making it work on any documentation site without configuration.

## How it works

```
You (URL + instruction)
        │
        ▼
   Claude AI (web_fetch)
   "Read the sidebar, find all doc links"
        │
        ▼
   URL list discovered
        │
        ▼
   Jina Reader (r.jina.ai)
   Converts each page → clean markdown
        │
        ▼
   📁 markdown files saved
```

1. **You provide a URL** — the entry page of a documentation section
2. 2. **Claude reads the page** — using the `web_fetch` tool, Claude fetches the HTML, understands the sidebar/navigation, and extracts all documentation links
   3. 3. **Jina converts to markdown** — each discovered page is fetched through [Jina Reader](https://r.jina.ai) and saved as clean markdown
     
      4. ## Installation
     
      5. ```bash
         git clone https://github.com/Hasan-ari/docs2md.git
         cd docs2md
         pip install -e .
         ```

         ## Setup

         Set your API keys as environment variables:

         ```bash
         export ANTHROPIC_API_KEY="sk-ant-..."
         export JINA_API_KEY="jina_..."  # optional, for higher rate limits
         ```

         ## Usage

         ### Scrape an entire documentation site

         ```bash
         # Basic — Claude auto-discovers all pages
         docs2md scrape https://developers.figma.com/docs/figma-mcp-server/

         # With extra instruction to filter pages
         docs2md scrape https://react.dev/reference/ -i "Only the React hooks pages"

         # Custom output dir + combined single file
         docs2md scrape https://docs.expo.dev/eas/workflows/ -o expo_docs --combine

         # Skip confirmation prompt
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
         | `-i, --instruction` | Extra guidance for Claude (e.g. "Only API pages") |
         | `--model` | Claude model (default: claude-sonnet-4) |
         | `-d, --delay` | Delay between requests in seconds (default: 1.5) |
         | `--combine` | Also create a single combined markdown file |
         | `-y, --yes` | Skip confirmation prompt |
         | `--anthropic-key` | Anthropic API key (or set `ANTHROPIC_API_KEY` env) |
         | `--jina-key` | Jina API key (or set `JINA_API_KEY` env) |

         ## Cost

         - **Claude API**: ~$0.01–0.05 per link discovery call (one call per site)
         - - **Jina Reader**: Free tier available (20 RPM), or use API key for higher limits
           - - **web_fetch**: No additional cost beyond standard token pricing
            
             - ## License
            
             - MIT
