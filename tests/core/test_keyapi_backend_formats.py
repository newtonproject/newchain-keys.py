import pytest

from newchain_keys import KeyAPI
from newchain_keys.backends import NativeECCBackend


@pytest.fixture(autouse=True)
def native_backend_env_var(monkeypatch):
    monkeypatch.setenv('ECC_BACKEND_CLASS', 'newchain_keys.backends.native.NativeECCBackend')


@pytest.mark.parametrize(
    'backend',
    (
        None,
        NativeECCBackend(),
        NativeECCBackend,
        'newchain_keys.backends.NativeECCBackend',
        'newchain_keys.backends.native.NativeECCBackend',
    ),
)
def test_supported_backend_formats(backend):
    keys = KeyAPI(backend=backend)
    assert isinstance(keys.backend, NativeECCBackend)
