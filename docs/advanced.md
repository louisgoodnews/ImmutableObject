# Advanced Topics

## Custom Validation

### Input Validation
```python
class NetworkConfig(ImmutableBaseObject):
    def __init__(self, host: str, port: int):
        if not isinstance(port, int) or port < 0 or port > 65535:
            raise ValueError("Invalid port number")
        if not isinstance(host, str) or not host:
            raise ValueError("Invalid host")
        
        super().__init__()
        self.host = host
        self.port = port
```

### Type Checking
```python
from typing import List, Dict

class ComplexConfig(ImmutableBaseObject):
    def __init__(self, routes: List[str], settings: Dict[str, str]):
        if not isinstance(routes, list):
            raise TypeError("routes must be a list")
        if not isinstance(settings, dict):
            raise TypeError("settings must be a dictionary")
            
        super().__init__()
        self.routes = routes
        self.settings = settings
```

## Nested Immutable Objects

### Creating Nested Structures
```python
class Address(ImmutableBaseObject):
    def __init__(self, street: str, city: str):
        super().__init__()
        self.street = street
        self.city = city

class Person(ImmutableBaseObject):
    def __init__(self, name: str, address: Address):
        if not isinstance(address, Address):
            raise TypeError("address must be an Address instance")
            
        super().__init__()
        self.name = name
        self.address = address
```

## Working with Collections

### Immutable Lists
```python
from typing import List, Tuple

class RouteConfig(ImmutableBaseObject):
    def __init__(self, routes: List[str]):
        super().__init__()
        # Convert mutable list to immutable tuple
        self.routes = tuple(routes)
```

### Immutable Dictionaries
```python
from typing import Dict
import types

class SettingsConfig(ImmutableBaseObject):
    def __init__(self, settings: Dict[str, str]):
        super().__init__()
        # Convert mutable dict to types.MappingProxyType
        self.settings = types.MappingProxyType(settings)
```

## Performance Considerations

### Memory Usage
- Immutable objects can't be modified in place
- Each modification creates a new instance
- Use appropriate data structures for large collections

### Caching
```python
from functools import lru_cache

class CachedConfig(ImmutableBaseObject):
    def __init__(self, data: Dict[str, str]):
        super().__init__()
        self._data = types.MappingProxyType(data)
    
    @lru_cache(maxsize=128)
    def get_processed_value(self, key: str) -> str:
        # Expensive computation here
        return self._data[key].upper()
```

## Threading and Concurrency

Immutable objects are inherently thread-safe because they cannot be modified after creation. This makes them excellent for use in concurrent programming:

```python
import threading
from typing import List

class SharedConfig(ImmutableBaseObject):
    def __init__(self, values: List[int]):
        super().__init__()
        self.values = tuple(values)  # Convert to immutable tuple

def worker(config: SharedConfig):
    # Safe to access from multiple threads
    for value in config.values:
        print(value)

# Usage
config = SharedConfig([1, 2, 3, 4, 5])
threads = [
    threading.Thread(target=worker, args=(config,))
    for _ in range(3)
]

for thread in threads:
    thread.start()
```

## Error Handling Patterns

### Custom Exceptions
```python
class ValidationError(Exception):
    pass

class ConfigurationError(Exception):
    pass

class ServerConfig(ImmutableBaseObject):
    def __init__(self, host: str, port: int):
        try:
            if not isinstance(port, int):
                raise ValidationError("Port must be an integer")
            if port < 0 or port > 65535:
                raise ValidationError("Port must be between 0 and 65535")
                
            super().__init__()
            self.host = host
            self.port = port
            
        except ValidationError as e:
            raise ConfigurationError(f"Invalid configuration: {str(e)}")
```

## Integration Patterns

### Factory Pattern
```python
class ConfigFactory:
    @staticmethod
    def create_development_config() -> 'ServerConfig':
        return ServerConfig("localhost", 8080)
    
    @staticmethod
    def create_production_config() -> 'ServerConfig':
        return ServerConfig("production.server", 80)
```

### Builder Pattern
```python
class ConfigBuilder:
    def __init__(self):
        self._host = "localhost"
        self._port = 8080
        
    def with_host(self, host: str) -> 'ConfigBuilder':
        self._host = host
        return self
        
    def with_port(self, port: int) -> 'ConfigBuilder':
        self._port = port
        return self
        
    def build(self) -> 'ServerConfig':
        return ServerConfig(self._host, self._port)
```
