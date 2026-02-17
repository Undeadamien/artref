from typing import Annotated, List

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from artref.core.config import COUNT_DEFAULT, COUNT_MAX, COUNT_MIN
from artref.core.main import fetch as core_fetch
from artref.core.types import ImageResponse, Source


class FetchParams(BaseModel):
    source: Source
    query: str
    count: int = Field(COUNT_DEFAULT, ge=COUNT_MIN, le=COUNT_MAX)


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}  # todo: replace with a proper message


@app.get("/fetch", response_model=List[ImageResponse])
async def fetch_images(params: Annotated[FetchParams, Query()]):
    try:
        images = await core_fetch(params.source, params.query, params.count)
        if not images:
            raise HTTPException(status_code=404, detail="No images found")
        return [ImageResponse(**img.__dict__) for img in images]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
