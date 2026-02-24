"""
Middleware for attaching jurisdiction context to every request.

Add ``geo_canon.jurisdictions.middleware.JurisdictionMiddleware`` to your
``MIDDLEWARE`` list. The middleware reads the jurisdiction from (in order):

1. ``request.session["jurisdiction"]``
2. ``GEOCANON.default_jurisdiction``
"""

from __future__ import annotations

from typing import Callable

from django.http import HttpRequest, HttpResponse

from ..settings import get_geocanon_settings


class JurisdictionMiddleware:
    """
    Attach ``request.jurisdiction`` to every request.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        settings = get_geocanon_settings()
        jurisdiction = getattr(request, "session", {}).get(
            "jurisdiction", settings.default_jurisdiction
        )
        request.jurisdiction = jurisdiction  # type: ignore[attr-defined]
        return self.get_response(request)
