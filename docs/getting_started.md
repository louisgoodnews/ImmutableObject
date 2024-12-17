# Getting Started with ImmutableObject

This guide will help you get started with using the ImmutableObject library in your Python projects.

## Installation

1. Install using pip:
```bash
pip install immutable-object
```

2. Or install from source:
```bash
git clone https://github.com/louisgoodnews/ImmutableObject.git
cd ImmutableObject
pip install -e .
```

## Quick Start

### Basic Usage

1. Import the necessary class:
```python
from core.base_object import ImmutableBaseObject
```

2. Create your immutable class:
```python
class UserSettings(ImmutableBaseObject):
    def __init__(self, username: str, theme: str = "light"):
        super().__init__()
        self.username = username
        self.theme = theme
```

3. Use your immutable object:
```python
settings = UserSettings(username="john_doe", theme="dark")
print(settings.username)  # Outputs: john_doe
```

### Advanced Features

#### Dictionary-style Access
```python
# Both styles work the same
print(settings.theme)      # Using attribute access
print(settings["theme"])   # Using dictionary access
```

#### Logging Integration
The ImmutableObject library comes with built-in logging:

```python
# Logging is automatically set up when you create an object
settings = UserSettings(username="john_doe")
# You'll see initialization logs in your application
```

## Common Patterns

### Configuration Objects
```python
class AppConfig(ImmutableBaseObject):
    def __init__(self, host: str, port: int, debug: bool = False):
        super().__init__()
        self.host = host
        self.port = port
        self.debug = debug

config = AppConfig("localhost", 8080, debug=True)
```

### Data Transfer Objects
```python
class UserDTO(ImmutableBaseObject):
    def __init__(self, id: int, name: str, email: str):
        super().__init__()
        self.id = id
        self.name = name
        self.email = email
```

## Best Practices

1. Always call `super().__init__()` in your class constructors
2. Use type hints for better code maintainability
3. Handle AttributeError exceptions when working with immutable objects
4. Use meaningful class and attribute names

## Next Steps

- Check out the [API Documentation](api.md) for detailed information
- Look at the [Examples](examples.md) for more use cases
- Read about [Advanced Topics](advanced.md) for complex scenarios
