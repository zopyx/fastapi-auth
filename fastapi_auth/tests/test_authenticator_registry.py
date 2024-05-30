from ..authenticator_registry import Authenticator, AuthenticatorRegistry


def test_authenticator_registry():
    class TestAuthenticator(Authenticator):
        name = "TestAuthenticator"

        def authenticate(self, request):
            return None

    registry = AuthenticatorRegistry()
    registry.add_authenticator(TestAuthenticator(), 0)

    assert len(registry.authenticators) == 1
    assert registry.authenticators[0].name == "TestAuthenticator"
    assert registry.authenticators[0].authenticate(None) is None


def test_authenticator_registry_with_multiple_authenticators():
    class TestAuthenticator1(Authenticator):
        name = "TestAuthenticator1"

        def authenticate(self, request):
            return None

    class TestAuthenticator2(Authenticator):
        name = "TestAuthenticator2"

        def authenticate(self, request):
            return None

    registry = AuthenticatorRegistry()
    registry.add_authenticator(TestAuthenticator1(), 0)
    registry.add_authenticator(TestAuthenticator2(), 1)

    assert len(registry.authenticators) == 2
    assert registry.authenticators[0].name == "TestAuthenticator1"
    assert registry.authenticators[1].name == "TestAuthenticator2"
    assert registry.authenticators[0].authenticate(None) is None
    assert registry.authenticators[1].authenticate(None) is None
