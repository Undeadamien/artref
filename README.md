# ArtRef

**ArtRef** is an asynchronous Python tool for fetching, organizing, and downloading image references from multiple sources efficiently.

**Motivation:**  
Searching for image references across multiple platforms can be slow and repetitive.
ArtRef centralizes this process, allowing you to quickly fetch, organize, and download images from multiple sources in a single workflow.

## Features

- **Multi-source search**: Scryfall, Unsplash, Wallhaven
- **Asynchronous**: Fast and efficient fetching
- **CLI**: Typer for easy command-line usage
- **API**: FastAPI server for programmatic access
- **Disk caching**: Avoid repeated downloads
- **Pluggable source system**: Add new image sources easily

## Installation

Install via pip:

```bash
pip install .
```

## Configuration

Optional .env (**Unsplash** only):

```
UNSPLASH_KEY=
```

Default config file:

```bash
./src/artref/core/config.py
```

## CLI Usage

> The syntax of the `query` argument depends on the source.

```bash
# Search 5 tree images on Unsplash
artref unsplash "tree"

# Search cards by artist on Scryfall
artref scryfall "artist:magali"

# Search images by Guweiz on Wallhaven
artref wallhaven "guweiz"

# Show help
artref --help
artref wallhaven --help
```

> Downloaded images will appear in the current working directory.  
> Each source generates a log file with metadata: `artref_YYMMDDHHMMSS.json`

## API

Start the server:

```bash
artref server
```

Example API request:

```bash
curl "http://127.0.0.1:8000/fetch?source=unsplash&query=example"
```

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
