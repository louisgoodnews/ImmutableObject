# ImmutableObject

A Python library that provides a robust implementation of immutable objects with attribute access and mapping interface support. This library is designed to help developers create objects that cannot be modified after initialization, ensuring data integrity and thread safety in their applications.

## Features

- **Immutable Objects**: Create objects that cannot be modified after initialization
- **Attribute Access**: Supports both attribute-style and dictionary-style access to object properties
- **Type Safety**: Built with Python's type hints for better IDE support and code safety
- **Logging Integration**: Built-in logging capabilities for better debugging and monitoring
- **Inheritance Support**: Extend the base classes to create your own immutable objects

## Installation

```bash
pip install immutable-object
```

## Usage

### Basic Usage

```python
from core.base_object import ImmutableBaseObject

# Create an immutable object
class Configuration(ImmutableBaseObject):
    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port

# Use the immutable object
config = Configuration(host="localhost", port=8080)

# Access attributes
print(config.host)  # Output: localhost
print(config["port"])  # Output: 8080

# Attempting to modify will raise an AttributeError
try:
    config.host = "newhost"  # Raises AttributeError
except AttributeError as e:
    print("Cannot modify immutable object")
```

### Inheritance

```python
class ServerConfig(ImmutableBaseObject):
    def __init__(self, host: str, port: int, max_connections: int):
        super().__init__()
        self.host = host
        self.port = port
        self.max_connections = max_connections
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Project Link: [https://github.com/louisgoodnews/ImmutableObject](https://github.com/louisgoodnews/ImmutableObject)