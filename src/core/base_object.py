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
        return f"{self.__class__.__name__}({', '.join(f'{key}={value}' for (key, value,) in self.__dict__.items())})"

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
