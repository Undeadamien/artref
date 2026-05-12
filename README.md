# ArtRef

**ArtRef** is an asynchronous Python tool for fetching, organizing, and downloading image references from multiple sources efficiently.

**Motivation:**  
Searching for image references across multiple platforms can be slow and repetitive.
ArtRef centralizes this process, allowing you to quickly fetch, organize, and download images from multiple sources in a single workflow.

## Features

- **Pydantic V2**: Robust data validation and settings management.
- **Asynchronous**: Fast and efficient fetching using `aiohttp`.
- **Resilient**: Automatic retries with exponential backoff for API rate limits.
- **CLI**: Typer for easy command-line usage.
- **API**: FastAPI server with shared logic (fetching and optional downloading).
- **Disk caching**: Integrated caching to avoid repeated API hits.

## Installation

```bash
pip install -e .
```

## Configuration

ArtRef uses Pydantic Settings. You can configure it via environment variables or a `.env` file:

```bash
# Required for Unsplash
UNSPLASH_KEY=your_key_here

# Optional overrides
SCRYFALL_URL=https://api.scryfall.com
SERVER_PORT=8000
```

## CLI Usage

```bash
# Fetch and download (default)
artref scryfall "artist:magali"

# Fetch and return JSON only (no download)
artref wallhaven "guweiz" --json

# Limit results
artref unsplash "forest" --count 5
```

## API

Start the server:

```bash
artref server
```

The API documentation is available at `http://127.0.0.1:8000/docs`.  
The `/fetch` endpoint supports an optional `download=true` parameter to trigger server-side downloading.

## Docker Support

Run the application using Docker:

```bash
# Build and start the API
docker compose up
```

The API will be available at `http://localhost:8000`.

## Roadmap

- [x] Add Docker support
- [ ] Enhance error handling
- [ ] Implement rate limiting and retry strategies
- [ ] Improve documentation, removing the placeholders
- [ ] Improve the API side
