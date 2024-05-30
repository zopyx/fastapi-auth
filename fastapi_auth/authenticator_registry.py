from abc import ABC, abstractmethod

from .users import User

from fastapi import Request
from typeguard import typechecked


class Authenticator(ABC):
    """Abstract base class for authenticators."""

    name: str = "Authenticator"

    @abstractmethod
    async def authenticate(self, request: Request) -> User | None:
        """Authenticate the user."""
        raise NotImplementedError()  # pragma: no cover


class AuthenticatorRegistry:
    """Registry for authenticators."""

    def __init__(self):
        self.authenticators = []

    @typechecked
    def add_authenticator(self, authenticator: Authenticator, position: int) -> None:
        """Add an authenticator to the registry."""
        self.authenticators.insert(position, authenticator)


AUTHENTICATOR_REGISTRY = AuthenticatorRegistry()
