"""
Main config file for FastAPI
"""

import logging
from logging import config as logging_config
import multiprocessing
import os
import random
import string
import time
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

load_dotenv()

from core import api
from core.registry import db, ENV

logging_config.fileConfig("./logging.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    process_name = multiprocessing.current_process().name
    logger.info(f"Process {process_name} started")
    if ENV != "PROD":
        for k, v in os.environ.items():
            logger.info(f"{k}={v}")

    await db.connect()

    logger.info("Server started")
    logger.info(f"ENV: {ENV}")
    logger.info("Open http://localhost:8000/api/ping")

    yield

    await db.close()
    logger.info("Server shutting down")


app = FastAPI(lifespan=lifespan)
app.include_router(api.router)

if ENV != "PROD":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["<domain-address>"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware for log requests and their answers
    :param request:
    :param call_next:
    :return:
    """
    idem = f"{random.choices(string.ascii_uppercase)}      {string.digits}"
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"
    logger.info(
        f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}"
    )

    return response


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="CORE API",
        version="0.1",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
