from __future__ import annotations

import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import router as v1_router
from app.core.handlers import install_exception_handlers


def create_app() -> FastAPI:
    app = FastAPI(title=settings.APP_TITLE)

    install_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=getattr(settings, "CORS_ORIGINS", ["*"]),
        allow_credentials=False,
        allow_headers=["*"],
        allow_methods=["*"],
    )

    @app.middleware("http")
    async def request_context_middleware(request: Request, call_next):
        """
        1) Correlation ID:
           - если клиент прислал X-Request-ID -> используем его
           - иначе генерим
        2) Timing:
           - пишем длительность запроса в заголовок
        """
        req_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
        request.state.request_id = req_id

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        response.headers["X-Request-ID"] = req_id
        response.headers["X-Response-Time-ms"] = f"{duration_ms:.2f}"
        return response

    app.include_router(v1_router, prefix="/api/v1")

    @app.get("/health", summary="Healthcheck")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()
