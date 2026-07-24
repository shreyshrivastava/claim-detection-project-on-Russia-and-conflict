"""Vercel Python runtime entrypoint for the FastAPI application."""

from claim_detection.api import app

__all__ = ["app"]
