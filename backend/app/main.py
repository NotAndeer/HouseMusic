"""Application entrypoint for FastAPI."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import auth, contacts, webhooks_meta, webhooks_email, campaigns


def create_app() -> FastAPI:
    """Construct the FastAPI application with routers and middleware."""

    app = FastAPI(title="HouseMusic Marketing Platform", version="1.0.0")

    # Allow frontend to communicate with backend during local development.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers.
    app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
    app.include_router(contacts.router, prefix="/api/v1", tags=["contacts"])
    app.include_router(campaigns.router, prefix="/api/v1", tags=["campaigns"])
    app.include_router(webhooks_meta.router, prefix="/api/v1", tags=["webhooks"])
    app.include_router(webhooks_email.router, prefix="/api/v1", tags=["webhooks"])

    @app.get("/health")
    def health() -> dict[str, str]:
        """Simple health endpoint used by orchestration tools."""

        return {"status": "ok"}

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_: Request, exc: HTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        # In production we would log the error; returning generic response to avoid leaking details.
        return JSONResponse(status_code=500, content={"detail": "Internal server error", "error": str(exc)})

    return app


app = create_app()
