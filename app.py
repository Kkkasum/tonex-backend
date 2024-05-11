from contextlib import asynccontextmanager
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from loguru import logger

from src.app.backend import api_router
from src.services.contracts import contracts_service


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator:
    await contracts_service.provider.start_up()
    logger.success('App is started up')
    yield
    await contracts_service.provider.close_all()
    logger.error('App is shutting down...')


app = FastAPI(
    title='TONEX App',
    lifespan=lifespan
)

origins = [
    '*'
    # 'https://roaring-bienenstitch-1d676b.netlify.app',
    # 'roaring-bienenstitch-1d676b.netlify.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['*']
)

app.include_router(api_router, prefix='/api', tags=['API'])
