import asyncio
from pprint import pprint

import typer

from artref.core.main import fetch

app = typer.Typer()


@app.command()
def scryfall(query: str):
    result = asyncio.run(fetch("scryfall", query))
    pprint(result)


@app.command()
def wallhaven(query: str):
    result = asyncio.run(fetch("wallhaven", query))
    pprint(result)


def main():
    app()
