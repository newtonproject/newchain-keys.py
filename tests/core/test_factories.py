from newchain_keys import keys
from newchain_keys.tools.factories import (
    PrivateKeyFactory,
    PublicKeyFactory,
)


def test_private_key_factory():
    actual = PrivateKeyFactory()
    assert actual == keys.PrivateKey(actual.to_bytes())


def test_public_key_factory():
    actual = PublicKeyFactory()
    assert actual == keys.PublicKey(actual.to_bytes())
