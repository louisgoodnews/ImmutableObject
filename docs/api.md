# API Documentation

## Core Classes

### BaseObject

The `BaseObject` class is the foundation of the ImmutableObject library. It provides basic attribute access and mapping interface functionality.

#### Methods

- `__init__()`: Initializes the BaseObject and sets up logging
- `__getattr__(name: str, default: Any = None) -> Any`: Gets an attribute value
- `__setattr__(name: str, value: Any)`: Sets an attribute value
- `__delattr__(name: str)`: Deletes an attribute

### ImmutableBaseObject

The `ImmutableBaseObject` class extends `BaseObject` to provide immutability guarantees.

#### Methods

- `__init__()`: Initializes the immutable object
- `__setattr__(name: str, value: Any)`: Raises AttributeError (immutable)
- `__setitem__(name: str, value: Any)`: Raises AttributeError (immutable)
- `__delattr__(name: str)`: Raises AttributeError (immutable)

## Usage Examples

### Creating an Immutable Configuration

```python
from core.base_object import ImmutableBaseObject

class Config(ImmutableBaseObject):
    def __init__(self, database_url: str, api_key: str):
        super().__init__()
        self.database_url = database_url
        self.api_key = api_key

# Usage
config = Config(
    database_url="postgresql://localhost:5432/db",
    api_key="secret"
)

# Access values
print(config.database_url)  # Using attribute access
print(config["api_key"])    # Using dictionary-style access
```

### Error Handling

```python
try:
    config.new_value = "test"  # Raises AttributeError
except AttributeError as e:
    print("Cannot modify immutable object")
```

## Best Practices

1. **Initialization**: Always call `super().__init__()` in your custom classes
2. **Type Hints**: Use type hints for better code maintainability
3. **Error Handling**: Always handle potential AttributeError exceptions
4. **Logging**: Use the built-in logger for debugging

## Advanced Usage

### Custom Validation

```python
class ValidatedConfig(ImmutableBaseObject):
    def __init__(self, port: int):
        super().__init__()
        if not isinstance(port, int) or port < 0 or port > 65535:
            raise ValueError("Invalid port number")
        self.port = port
```
