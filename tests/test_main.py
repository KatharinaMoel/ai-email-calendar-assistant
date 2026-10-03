import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from app.main import app, verify_signature


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_nylas_challenge() -> None:
    response = client.get("/events", params={"challenge": "week-one"})
    assert response.status_code == 200
    assert response.text == "week-one"


def test_signature_verification() -> None:
    body = json.dumps({"event": "message.created"}).encode()
    signature = hmac.new(b"secret", body, hashlib.sha256).hexdigest()
    assert verify_signature(body, b"secret", signature)
    assert not verify_signature(body, b"secret", "incorrect")
