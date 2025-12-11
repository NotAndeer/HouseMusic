"""Health check endpoint for infrastructure monitoring."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    """Return service health status and version.
    
    Used by Docker, Kubernetes, and uptime monitors.
    """
    return {
        "status": "ok",
        "version": "1.0.0"
    }