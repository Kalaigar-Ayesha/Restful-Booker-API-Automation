from jsonschema import validate
from jsonschema.exceptions import ValidationError

# Simple wrapper so tests can import a single function
def assert_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as e:
        raise AssertionError(f"JSON schema validation failed: {e.message}\nPath: {list(e.path)}\nSchema path: {list(e.schema_path)}")
