import pytest

from modules.gateway.gateway import (
    dry_run_gateway_response,
    get_gateway_health,
    list_gateway_models,
    normalize_gateway_request,
)


def test_gateway_health_dry_run() -> None:
    health = get_gateway_health(dry_run=True)

    assert health["ok"] is True
    assert health["mode"] == "dry-run"
    assert health["bind"] == "127.0.0.1"
    assert health["server"] == "not_started"
    assert health["providers"] == "not_called"
    assert health["secrets"] == "not_read"
    assert "POST /v1/responses" in health["routes"]


def test_gateway_models_dry_run() -> None:
    models = list_gateway_models(dry_run=True)

    assert models == [
        {
            "id": "comptext-dry-run-model",
            "provider": "comptext-local",
            "state": "not_configured",
            "capabilities": ["text", "tools_planned"],
        }
    ]


def test_normalize_gateway_request_valid_input() -> None:
    normalized = normalize_gateway_request(
        {
            "model": "comptext-dry-run-model",
            "messages": [{"role": "user", "content": "hello"}],
            "tools": [],
            "metadata": {"run_id": "sample"},
        }
    )

    assert normalized == {
        "mode": "dry-run",
        "provider": "comptext-local",
        "model": "comptext-dry-run-model",
        "messages": [{"role": "user", "content": "hello"}],
        "tools": [],
        "metadata": {"run_id": "sample"},
    }


def test_normalize_gateway_request_defaults_explicit_null_values() -> None:
    normalized = normalize_gateway_request(
        {
            "model": None,
            "messages": None,
            "tools": None,
            "metadata": None,
        }
    )

    assert normalized == {
        "mode": "dry-run",
        "provider": "comptext-local",
        "model": "comptext-dry-run-model",
        "messages": [],
        "tools": [],
        "metadata": {},
    }


def test_normalize_gateway_request_rejects_non_object_input() -> None:
    with pytest.raises(ValueError, match="root must be an object"):
        normalize_gateway_request(["not", "an", "object"])  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"messages": "hello"}, "messages must be a list"),
        ({"tools": {"name": "tool"}}, "tools must be a list"),
        ({"model": 123}, "model must be a string"),
        ({"metadata": "sample"}, "metadata must be an object"),
    ],
)
def test_normalize_gateway_request_rejects_invalid_field_types(
    payload: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        normalize_gateway_request(payload)


def test_dry_run_gateway_response_never_calls_providers_network_or_secrets() -> None:
    response = dry_run_gateway_response({"messages": [{"role": "user", "content": "hello"}]})

    assert response["ok"] is True
    assert response["providers"] == "not_called"
    assert response["network"] == "not_called"
    assert response["secrets"] == "not_read"
    assert response["evidence"] == {"planned": True}
    assert response["request"]["provider"] == "comptext-local"  # type: ignore[index]
