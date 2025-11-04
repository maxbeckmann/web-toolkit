webtoolkit
==========

``webtoolkit`` lets you treat HTTP requests and responses as structured Python
classes. Describe a raw HTTP exchange inside a docstring, declare arguments for
the dynamic portions, and the package handles formatting, mutation, and
response parsing for you.

Installation
------------

The project uses a standard ``src`` layout and ships with a ``pyproject.toml``.
You can install it in editable mode while developing:

```
python -m pip install --upgrade pip
python -m pip install -e .
```

After installation the ``webtoolkit`` package becomes importable and a
``webtoolkit-example`` console script is available.

Quick start
-----------

Create a request/response pair by subclassing :class:`webtoolkit.Request`:

```python
from webtoolkit import JsonBodyValue, Request


class Login(Request):
    """
    POST /login HTTP/1.1
    Host: example.com
    Content-Type: application/json

    {"username": "demo@example.com", "password": "hunter2"}
    """

    username = JsonBodyValue("$.username")

    class Response(Request.Response):
        token = JsonBodyValue("$.token")
```

Pass overrides while instantiating the request, inspect the actual HTTP message
that will be sent, and parse the resulting response:

```python
login = Login(username="alice@example.com")
prepared = login.prepare()
login.apply_arguments(prepared)
from webtoolkit import format_request  # fan-out helpers
print("\n".join(format_request(prepared)))  # doctest: +SKIP

response = login.send()
print(response.token)
```

Examples
--------

Run the packaged demo for a guided tour that does not require network access:

```
python -m webtoolkit
# or
webtoolkit-example
```
