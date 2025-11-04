"""
Public package interface for webtoolkit.

The package focuses on defining HTTP requests as reusable Python classes with
rich argument handling and response parsing helpers.
"""

from .base import (
    Argument,
    Bearer,
    CookieArgument,
    FormParameter,
    GetParameter,
    Header,
    JsonBodyValue,
    LambdaArgument,
    Request,
    Session,
    XmlBodyValue,
)
from .parsing import (
    carve_string,
    format_head,
    format_request,
    format_response,
    parse_http_request,
    strip_unnecessary_whitespace,
)
from .url_parsing import get_url_parameter

__all__ = [
    "Argument",
    "Bearer",
    "CookieArgument",
    "FormParameter",
    "GetParameter",
    "Header",
    "JsonBodyValue",
    "LambdaArgument",
    "Request",
    "Session",
    "XmlBodyValue",
    "carve_string",
    "format_head",
    "format_request",
    "format_response",
    "get_url_parameter",
    "parse_http_request",
    "strip_unnecessary_whitespace",
]

__version__ = "0.1.0"
