from typing import Annotated, List

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from artref.core.config import COUNT_DEFAULT, COUNT_MAX, COUNT_MIN
from artref.core.main import fetch as core_fetch
from artref.core.types import ImageResponse, Source


class FetchParams(BaseModel):
    source: Source
    query: str
    count: int = Field(COUNT_DEFAULT, ge=COUNT_MIN, le=COUNT_MAX)


app = FastAPI(title="ArtRef", description="Image reference fetcher")


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


@app.get("/sources")
def list_sources():
    return [source.value for source in Source]


@app.get(
    "/fetch",
    response_model=List[ImageResponse],
    summary="Fetch images from a source",
    description="Fetch image references from the selected source",
)
async def fetch_images(params: Annotated[FetchParams, Query()]):
    images = await core_fetch(params.source, params.query, params.count)
    if not images:
        raise HTTPException(status_code=404, detail="No images found")
    return [ImageResponse(**img.__dict__) for img in images]
