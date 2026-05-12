import logging
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Annotated, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

from artref.core.models import FetchParams as CoreFetchParams
from artref.core.models import Reference, Source
from artref.core.service import run_fetch
from artref.core.session import close_session

logger = logging.getLogger(__name__)


class APIFetchParams(CoreFetchParams):
    download: bool = False


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await close_session()


app = FastAPI(title="ArtRef", description="Image reference fetcher", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/sources")
def list_sources():
    return [source.value for source in Source]


@app.get(
    "/fetch",
    response_model=List[Reference],
    summary="Fetch images from a source",
    description="Fetch image references from the selected source",
)
async def fetch_images(params: Annotated[APIFetchParams, Query()]):
    download_folder = None
    if params.download:
        timestamp = datetime.now().strftime("%y%m%d%H%M%S")
        download_folder = Path.cwd() / f"artref_{timestamp}"

    images = await run_fetch(params.source, params.query, params.count, download_folder)
    if not images:
        raise HTTPException(status_code=404, detail="No images found")
    return images
