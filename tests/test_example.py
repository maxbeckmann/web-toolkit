import json

from webtoolkit.example import EchoExampleRequest, main


def test_demo_returns_payload():
    payload = main()

    assert payload["json"]["message"] == "Hello, webtoolkit!"
    assert payload["json"]["repeat"] == 3


def test_request_arguments_are_applied():
    req = EchoExampleRequest(message="Hi!", repeat=1, session_id="xyz")
    prepared = req.prepare()
    req.apply_arguments(prepared)

    body = prepared.body.decode() if isinstance(prepared.body, bytes) else prepared.body
    assert body is not None
    assert json.loads(body) == {"message": "Hi!", "repeat": 1}
    assert prepared.headers["Cookie"] == "sessionid=xyz"
