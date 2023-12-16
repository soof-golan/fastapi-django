from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

from fastapi import FastAPI


class State(TypedDict):
    fake_db: dict[str, str]


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[State]:
    yield {
        "fake_db": {
            "1": "one",
            "2": "two",
        }
    }
