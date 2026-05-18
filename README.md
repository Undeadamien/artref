# ArtRef

![Python](https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FASTAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Pydantic](https://img.shields.io/badge/PYDANTIC-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Docker](https://img.shields.io/badge/DOCKER-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-000000?style=for-the-badge&logo=typer&logoColor=white)
![aiohttp](https://img.shields.io/badge/aiohttp-2C5BB4?style=for-the-badge&logo=aiohttp&logoColor=white)

Async image reference fetcher for Unsplash, Wallhaven, and Scryfall. Use it via CLI or API.

## Features

- Fetch from Unsplash, Wallhaven, and Scryfall
- Async HTTP with retries and exponential backoff
- CLI (Typer) and API (FastAPI) sharing the same core
- In-memory caching via aiocache
- Optional download to local folder with metadata log
- Docker Compose

## Quick Start

```bash
pip install -e .
```

- CLI: `artref --help`
- API: `artref server`, docs at `http://localhost:8000/docs`

## Testing

```bash
make test       # offline
make test-all   # full suite
```

See `Makefile` for all available commands.

## Configuration

Set `UNSPLASH_KEY` in `.env` or environment (required for Unsplash only).
