import pytest

from modules.validation.schema_validator import validate_json_schema_instance


@pytest.mark.parametrize(
    ("schema", "instance"),
    [
        ({"type": "boolean"}, True),
        ({"type": "integer"}, 3),
        ({"type": "number"}, 3.5),
        ({"type": "null"}, None),
    ],
)
def test_validate_json_schema_instance_supports_standard_types(schema, instance) -> None:
    validate_json_schema_instance(schema, instance)


def test_validate_json_schema_instance_rejects_unsupported_types() -> None:
    with pytest.raises(ValueError, match="unsupported schema type"):
        validate_json_schema_instance({"type": "date"}, "2026-07-05")


def test_validate_json_schema_instance_does_not_treat_boolean_as_integer() -> None:
    with pytest.raises(ValueError, match="must be integer"):
        validate_json_schema_instance({"type": "integer"}, True)
