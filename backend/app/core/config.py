"""Configuration module for backend settings.

This module centralizes runtime configuration using Pydantic's
``BaseSettings`` so values can be pulled from environment variables,
``.env`` files or defaults. The ``Settings`` object is imported across the
application to configure the database engine, Redis, OAuth flows and
security components like JWT.
"""

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    The values defined here are intentionally explicit to document how the
    system should be configured in production. Defaults are development-
    friendly but should be overridden through environment variables when
    deploying. Pydantic automatically reads environment variables matching
    the attribute names (case insensitive) or from a ``.env`` file if
    present.
    """

    database_url: str = Field(
        "postgresql+psycopg2://postgres:postgres@db:5432/housemusic",
        description="SQLAlchemy URL for the PostgreSQL database.",
    )
    redis_url: str = Field(
        "redis://redis:6379/0",
        description="Redis connection string used by Celery for broker/results.",
    )

    jwt_secret: str = Field("super-secret-key", description="Secret key for JWT signing")
    jwt_algorithm: str = Field("HS256", description="JWT signing algorithm")
    jwt_expiration_minutes: int = Field(60 * 24, description="Expiration window for access tokens")

    email_api_key: str = Field(
        "changeme-email", description="API key for transactional email providers"
    )
    meta_api_key: str = Field(
        "changeme-meta", description="API key for Meta integrations"
    )

    oauth_redirect_uri: str = Field(
        "http://localhost:3000/oauth/callback",
        description="Frontend redirect URI after OAuth consent.",
    )
    oauth_client_id: str = Field("meta-client", description="OAuth client id for Meta")
    oauth_client_secret: str = Field(
        "meta-secret", description="OAuth client secret for Meta"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Reusable settings instance so all modules share the same configuration.
settings = Settings()
