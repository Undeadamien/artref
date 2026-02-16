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

> Using the **Unsplash API**, if you intend to download an image at `path`, please also make a request at `download_location`.  
> For more information: [Unsplash API Guidelines](https://help.unsplash.com/en/articles/2511258-guideline-triggering-a-download)

## Roadmap

- [ ] Add Docker support
- [ ] Enhance error handling
- [ ] Ensure Unsplash `download_location` is triggered correctly
- [ ] Implement rate limiting and retry strategies
- [ ] Improve documentation, removing the placeholders
- [ ] Improve the API side
