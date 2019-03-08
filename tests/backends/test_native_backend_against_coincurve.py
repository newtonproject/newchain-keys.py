import pytest

from hypothesis import (
    given,
    settings,
    strategies as st,
)

from eth_utils import (
    int_to_big_endian,
    keccak,
)

from newchain_keys.exceptions import (
    BadSignature,
)
from newchain_keys.utils.padding import (
    pad32,
)

from newchain_keys import KeyAPI
from newchain_keys.backends import CoinCurveECCBackend
from newchain_keys.backends import NativeECCBackend
from newchain_keys.constants import (
    SECPK1_N,
)


private_key_st = st.integers(min_value=1, max_value=SECPK1_N).map(
    int_to_big_endian,
).map(pad32)


message_hash_st = st.binary(min_size=32, max_size=32)
signature_st = st.binary(min_size=65, max_size=65)


MSG = b'message'
MSGHASH = keccak(MSG)

MAX_EXAMPLES = 200


@pytest.fixture
def native_key_api():
    return KeyAPI(backend=NativeECCBackend())


@pytest.fixture
def coincurve_key_api():
    return KeyAPI(backend=CoinCurveECCBackend())


@given(
    private_key_bytes=private_key_st,
    direction=st.one_of(
        st.just('coincurve-to-native'),
        st.just('native-to-coincurve'),
    ),
)
@settings(max_examples=MAX_EXAMPLES)
def test_public_key_generation_is_equal(private_key_bytes,
                                        direction,
                                        native_key_api,
                                        coincurve_key_api):
    if direction == 'coincurve-to-native':
        backend_a = coincurve_key_api
        backend_b = native_key_api
    elif direction == 'native-to-coincurve':
        backend_b = coincurve_key_api
        backend_a = native_key_api
    else:
        assert False, "invariant"

    public_key_a = backend_a.PrivateKey(private_key_bytes).public_key
    public_key_b = backend_b.PrivateKey(private_key_bytes).public_key

    assert public_key_a == public_key_b


@given(
    private_key_bytes=private_key_st,
    message_hash=message_hash_st,
    direction=st.one_of(
        st.just('coincurve-to-native'),
        st.just('native-to-coincurve'),
    ),
)
@settings(max_examples=MAX_EXAMPLES)
def test_native_to_coincurve_recover(private_key_bytes,
                                     message_hash,
                                     direction,
                                     native_key_api,
                                     coincurve_key_api):
    if direction == 'coincurve-to-native':
        backend_a = coincurve_key_api
        backend_b = native_key_api
    elif direction == 'native-to-coincurve':
        backend_b = coincurve_key_api
        backend_a = native_key_api
    else:
        assert False, "invariant"

    pk_a = backend_a.PrivateKey(private_key_bytes)
    signature_a = backend_a.ecdsa_sign(message_hash, pk_a)

    public_key_b = backend_b.ecdsa_recover(message_hash, signature_a)
    assert public_key_b == pk_a.public_key


@given(
    message_hash=message_hash_st,
    signature_bytes=signature_st,
    direction=st.one_of(
        st.just('coincurve-to-native'),
        st.just('native-to-coincurve'),
    ),
)
@settings(max_examples=MAX_EXAMPLES)
def test_coincurve_to_native_invalid_signatures(message_hash,
                                                signature_bytes,
                                                direction,
                                                native_key_api,
                                                coincurve_key_api):
    if direction == 'coincurve-to-native':
        backend_a = coincurve_key_api
        backend_b = native_key_api
    elif direction == 'native-to-coincurve':
        backend_b = coincurve_key_api
        backend_a = native_key_api
    else:
        assert False, "invariant"

    try:
        signature_a = backend_a.Signature(signature_bytes)
    except BadSignature:
        is_bad_signature = True
    else:
        is_bad_signature = False

    if is_bad_signature:
        with pytest.raises(BadSignature):
            backend_b.Signature(signature_bytes)
        return
    try:
        public_key_a = backend_a.ecdsa_recover(message_hash, signature_a)
    except BadSignature:
        is_bad_recovery = True
    else:
        is_bad_recovery = False

    if is_bad_recovery:
        with pytest.raises(BadSignature):
            backend_b.ecdsa_recover(message_hash, signature_a)
        return

    public_key_b = backend_b.ecdsa_recover(message_hash, signature_a)

    assert public_key_b == public_key_a
