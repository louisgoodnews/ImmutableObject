from typing import *

from logger.logger import Logger


class BaseObject:
    """
    A base class for creating objects that support attribute access
    and also provide a mapping interface.

    This class allows dynamic attribute assignment and supports dictionary-like access.

    Attributes:
        logger (Logger): An instance of the Logger class to log messages in this class.
    """

    def __init__(self) -> None:
        """
        Initializes the BaseObject class.

        This method logs a message to indicate that the object has been created and its being initialized.
        """
        self._logger: Logger = Logger.get_logger(self.__class__.__name__)
        self._logger.info(message=f"Initialized {self.__class__.__name__}...")

    def __delattr__(
        self,
        name: str,
        /,
    ) -> None:
        """
        Deletes an attribute from the object.

        :param name: The attribute name to delete.
        """
        del self.__dict__[name]

    def __getattr__(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Gets the value of an attribute or returns a default if not found.

        :param name: The attribute name to retrieve.
        :param default: The default value to return if the attribute is not found.
        :return: The attribute's value or the default.
        """
        return getattr(
            self.__dict__,
            name,
            default,
        )

    def __getitem__(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieves a value from the object's internal dictionary.

        :param name: The key to retrieve.
        :param default: The value to return if the key is not found.
        :return: The value associated with the key or the default.
        """
        return self.__dict__.get(
            name,
            default,
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the object.
        """
        return self.__str__()

    def __setattr__(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Sets an attribute on the object.

        :param name: The attribute name.
        :param value: The value to set.
        """
        self.__dict__[name] = value

    def __setitem__(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Sets a value in the object's internal dictionary.

        :param name: The key to set.
        :param value: The value to associate with the key.
        """
        self.__dict__[name] = value

    def __str__(self) -> str:
        """
        Returns a string representation of the object, listing all attributes and values.
        """
        return f"<{self.__class__.__name__}({', '.join(f'{key}={value}' for (key, value,) in self.__dict__.items())})>"

    def to_dict(
        self,
        exclude: Optional[Iterable[str]] = None,
    ) -> Dict[str, Any]:
        """
        Returns a dictionary representation of the object, optionally excluding specified attributes.

        :param exclude: An iterable of attribute names to exclude from the dictionary.
        :return: A dictionary with the object's attributes as key-value pairs.
        """
        return {
            key: value
            for (
                key,
                value,
            ) in self.__dict__.items()
            if key not in exclude or []
        }


class BaseObjectBuilder(BaseObject):
    """
    A base class for creating object builders that support dynamic attribute assignment
    and also provide a mapping interface.

    This class is a specialized version of BaseObject that is designed to be used
    as a builder for other objects. It provides a configuration dictionary that can be used to
    store the attributes of the object being built.

    The configuration dictionary is a dictionary of key-value pairs, where each key is an attribute
    name and the value is the attribute value.

    The BaseObjectBuilder class also provides a build method that can be overridden in subclasses to
    build the final object based on the configuration.
    """

    def __init__(self) -> None:
        """
        Initializes the BaseObjectBuilder class.

        The BaseObjectBuilder class is a specialized version of BaseObject that is designed to be used
        as a builder for other objects. It provides a configuration dictionary that can be used to
        store the attributes of the object being built.

        The configuration dictionary is a dictionary of key-value pairs, where each key is an attribute
        name and the value is the attribute value.

        The BaseObjectBuilder class also provides a build method that can be overridden in subclasses to
        build the final object based on the configuration.

        :return: The initialized BaseObjectBuilder object.
        """
        super().__init__()
        self._configuration: Dict[str, Any] = {}

    @property
    def configuration(self) -> Dict[str, Any]:
        """
        Returns the current configuration of the builder.

        The configuration is a dictionary of key-value pairs, where each key is an attribute name and
        the value is the attribute value.

        :return: The current configuration of the builder.
        """
        return self._configuration

    @configuration.setter
    def configuration(
        self,
        value: Dict[str, Any],
    ) -> None:
        """
        Updates the builder's configuration with the provided dictionary of values.

        :param value: A dictionary of key-value pairs to update the configuration.
        :return: The updated builder object.
        """
        self._configuration = value

    def build(self) -> Any:
        """
        Builds an object based on the builder's configuration.

        :return: An object of a type determined by the builder's configuration.
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement the 'build' method."
        )

    def kwargs(
        self,
        **kwargs,
    ) -> Self:
        """
        Updates the builder's configuration with the provided keyword arguments.

        :param kwargs: Additional keyword arguments to update the configuration.
        :return: The updated builder object.
        """
        self._configuration.update(kwargs)
        return self


class BaseObjectManager(BaseObject):
    """
    A base class for implementing managers for objects of type
    :py:class:`BaseObject`.

    The manager provides a cache for objects and a factory for creating new
    objects. The cache expires after a configurable time limit.

    Attributes:
        cache (Dict[str, Any]): The cache of objects.
        timestamp (datetime): The timestamp of the last cache update.
        time_limit (int): The time limit in seconds for the cache.
    """

    def __init__(self, time_limit: int = 300,) -> None:
        """
        Initializes a BaseObjectManager.

        :param time_limit: The time limit in seconds for the cache. Defaults to 300 seconds.
        """
        super().__init__()

        self._cache: Dict[str, Any] = {}
        self._time_limit: int = time_limit
        self._timestamp: datetime = datetime.now()

    @property
    def cache(self) -> Dict[str, Any]:
        """
        Gets the current cache of objects.

        :return: The current cache of objects.
        """
        return self._cache

    @property
    def time_limit(self) -> int:
        """
        Gets the time limit in seconds for the cache.

        :return: The time limit in seconds for the cache.
        """
        return self._time_limit

    @property
    def timestamp(self) -> datetime:
        """
        Gets the timestamp of the last cache update.

        :return: The timestamp of the last cache update.
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime,) -> None:
        """
        Sets the timestamp of the last cache update.

        :param value: The new timestamp value.
        """
        self._timestamp = value

    def _add_to_cache_(self, key: str, value: Any,) -> None:
        """
        Adds the specified entry to the cache.

        :param key: The key of the entry.
        :param value: The value of the entry.
        """
        self._cache[key] = value

        self._logger.info(message=f"Added {key} to cache.")

    def _check_time_limit_(self) -> bool:
        """
        Checks if the time limit has been reached.

        :return: True if the time limit has been reached, False otherwise.
        """
        return (datetime.now() - self._timestamp).total_seconds() > self._time_limit

    def _flush_cache_(self, force: bool = False,) -> None:
        """
        Flushes the cache.

        If the time limit has been reached or if the force parameter is True,
        the cache is flushed by clearing its contents and resetting the timestamp.
        This method is intended to be called internally by the cache property
        setter.

        :param force: Whether to flush the cache regardless of the time limit.
        :type force: bool
        """
        if force or self._check_time_limit_():
            self._cache = {}
            self._timestamp = datetime.now()

            self._logger.info(message="Flushed cache.")

    def _get_from_cache_(self, key: str,) -> Any:
        """
        Retrieves the value associated with the specified key from the cache.

        :param key: The key of the entry.
        :return: The value associated with the key.

        If the key is not found in the cache, a KeyError is raised.
        """
        return self._cache[key]

    def _is_in_cache_(self, key: str,) -> bool:
        """
        Checks if the specified key is in the cache.

        :param key: The key to check.
        :return: True if the key is in the cache, False otherwise.
        """
        return key in self._cache

    def _remove_from_cache_(self, key: str,) -> None:
        """
        Removes the specified key from the cache.

        This method is intended to be called internally by the cache property
        setter.

        :param key: The key to remove.
        """
        del self._cache[key]

        self._logger.info(message=f"Removed {key} from cache.")

    def _update_in_cache_(self, key: str, value: Any,) -> None:
        """
        Updates the value associated with the specified key in the cache.

        This method is intended to be called internally by the cache property
        setter.

        :param key: The key of the entry.
        :param value: The new value of the entry.
        """
        self._cache[key] = value

        self._logger.info(message=f"Updated {key} in cache.")


class ImmutableBaseObject(BaseObject):
    """
    A base class for creating objects that support attribute access
    and also provide a mapping interface.

    This class is immutable, meaning attributes cannot be added, modified, or deleted.

    Inherits from the BaseObject class.

    Attributes:
        logger (Logger): An instance of the Logger class to log messages in this class.
    """

    def __init__(self) -> None:
        """
        Initializes the ImmutableBaseObject class.

        This method does not allow attribute assignment, as it is immutable.
        """
        super().__init__()

    def __setattr__(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Prevents attribute assignment.

        :param name: The attribute name.
        :param value: The value to assign.
        :raises AttributeError: Always raises an exception because the class is immutable.
        """
        self._logger.error(
            message=f"Cannot set attribute '{name}' in {self.__class__.__name__}."
        )

        raise AttributeError(f"'{self.__class__.__name__}' is immutable.")

    def __setitem__(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Prevents setting items in the internal dictionary.

        :param name: The key to set.
        :param value: The value to associate with the key.
        :raises AttributeError: Always raises an exception because the class is immutable.
        """
        self._logger.error(
            message=f"Cannot set attribute '{name}' in {self.__class__.__name__}."
        )

        raise AttributeError(f"'{self.__class__.__name__}' is immutable.")

    def __delattr__(
        self,
        name: str,
    ) -> None:
        """
        Prevents attribute deletion.

        :param name: The attribute name to delete.
        :raises AttributeError: Always raises an exception because the class is immutable.
        """
        self._logger.warn(
            message=f"Cannot set attribute '{name}' in {self.__class__.__name__}."
        )

        raise AttributeError(f"'{self.__class__.__name__}' is immutable.")
