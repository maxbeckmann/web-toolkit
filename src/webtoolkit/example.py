"""
Command-line demonstration for the :mod:`webtoolkit` package.

The example mirrors how you can express an HTTP transaction as a pair of
Python classes. To keep the demonstration offline-friendly, the ``send``
method fabricates a deterministic ``requests.Response`` instance instead of
performing a real network call.
"""

from __future__ import annotations

import json
from typing import Any, Dict

import requests

from .base import CookieArgument, JsonBodyValue, Request
from .parsing import format_request, format_response


class EchoExampleRequest(Request):
    """
    POST /post HTTP/1.1
    Host: httpbin.org
    Content-Type: application/json
    Accept: application/json
    Cookie: sessionid=12345

    {"message": "Hello, World!", "repeat": 1}
    """

    message = JsonBodyValue("$.message")
    repeat = JsonBodyValue("$.repeat")
    session_id = CookieArgument("sessionid")

    class Response(Request.Response):
        echoed_message = JsonBodyValue("$.json.message")
        cookie_header = JsonBodyValue("$.headers.Cookie")

    def send(self, session: requests.Session | None = None, **kwargs: Any):
        """
        Build a fake ``requests.Response`` instance to showcase the parsing
        helpers without relying on an external HTTP service.
        """

        prepared = self.prepare()
        self.apply_arguments(prepared)

        response = requests.Response()
        response.status_code = 200
        response.reason = "OK"
        response.headers = {
            "Content-Type": "application/json",
            "X-Demo": "webtoolkit",
        }
        response._content = json.dumps(
            {
                "json": {"message": self.message, "repeat": self.repeat},
                "headers": {"Cookie": f"sessionid={self.session_id}"},
            }
        ).encode()
        response.url = self.url
        response.request = prepared

        response.__class__ = self.__class__.Response
        return response


def main() -> Dict[str, Any]:
    """
    Run the example: build the request, apply argument overrides, and show the
    formatted request/response pair. Returns the parsed response payload so
    unit tests can assert against it.
    """

    request = EchoExampleRequest(message="Hello, webtoolkit!", repeat=3, session_id="abc")
    prepared = request.prepare()
    request.apply_arguments(prepared)

    response = request.send()

    print("== Request ==")
    for line in format_request(prepared):
        print(line)

    print("\n== Response ==")
    for line in format_response(response):
        print(line)

    payload: Dict[str, Any] = response.json()
    return payload


if __name__ == "__main__":  # pragma: no cover
    main()
