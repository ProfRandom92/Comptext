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


def test_validate_json_schema_instance_pattern_search_semantics() -> None:
    # pattern "foo" accepts "xxfooyy" (search semantics)
    validate_json_schema_instance({"type": "string", "pattern": "foo"}, "xxfooyy")

    # pattern "^foo$" accepts "foo"
    validate_json_schema_instance({"type": "string", "pattern": "^foo$"}, "foo")

    # pattern "^foo$" rejects "xxfooyy"
    with pytest.raises(ValueError, match="does not match pattern"):
        validate_json_schema_instance({"type": "string", "pattern": "^foo$"}, "xxfooyy")


def test_validate_json_schema_instance_pattern_failures() -> None:
    # pattern as non-string raises ValueError
    with pytest.raises(ValueError, match="pattern must be a string"):
        validate_json_schema_instance({"type": "string", "pattern": 123}, "some_string")

    # invalid regex pattern raises ValueError
    with pytest.raises(ValueError, match="invalid regex pattern"):
        validate_json_schema_instance({"type": "string", "pattern": "[invalid"}, "some_string")


def test_validate_json_schema_instance_min_items() -> None:
    # Should pass when count of items >= minItems
    validate_json_schema_instance({"type": "array", "minItems": 2}, [1, 2])
    validate_json_schema_instance({"type": "array", "minItems": 2}, [1, 2, 3])

    # Should raise ValueError when count of items < minItems
    with pytest.raises(ValueError, match="must have at least 2 items"):
        validate_json_schema_instance({"type": "array", "minItems": 2}, [1])


def test_validate_json_schema_instance_required_fields() -> None:
    schema = {
        "type": "object",
        "required": ["a", "b"]
    }
    validate_json_schema_instance(schema, {"a": 1, "b": 2})

    with pytest.raises(ValueError, match=r"\$.a is required"):
        validate_json_schema_instance(schema, {"b": 2})


def test_validate_json_schema_instance_properties() -> None:
    schema = {
        "type": "object",
        "properties": {
            "a": {"type": "integer"},
            "b": {"type": "string"}
        }
    }
    validate_json_schema_instance(schema, {"a": 1, "b": "hello"})

    with pytest.raises(ValueError, match=r"\$.a must be integer"):
        validate_json_schema_instance(schema, {"a": "not_an_int", "b": "hello"})
