from contextlib import asynccontextmanager
from typing import AsyncIterator, TypedDict

from fastapi import FastAPI


class State(TypedDict):
    """Application state

    Accessible in through `request.state.foo`

    TODO: Add any application state here.
    """

    a: int


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[State]:
    yield {
        "a": 1,
    }
