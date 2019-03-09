import pytest

from eth_utils import (
    decode_hex,
    keccak,
)


MSG = b'message'
MSGHASH = keccak(MSG)


# This is a sample of signatures generated with a known-good implementation of the ECDSA
# algorithm, which we use to test our ECC backends. If necessary, it can be generated from scratch
# with the following code:
"""
from devp2p import crypto
from eth_utils import encode_hex
msg = b'message'
msghash = crypto.sha3(b'message')
for secret in ['alice', 'bob', 'eve']:
    print("'{}': dict(".format(secret))
    privkey = crypto.mk_privkey(secret)
    pubkey = crypto.privtopub(privkey)
    print("    privkey='{}',".format(encode_hex(privkey)))
    print("    pubkey='{}',".format(encode_hex(crypto.privtopub(privkey))))
    ecc = crypto.ECCx(raw_privkey=privkey)
    sig = ecc.sign(msghash)
    print("    sig='{}',".format(encode_hex(sig)))
    print("    raw_sig='{}')".format(crypto._decode_sig(sig)))
    assert crypto.ecdsa_recover(msghash, sig) == pubkey
"""


SECRETS = {
    "alice": dict(
        privkey=decode_hex('0x9c0257114eb9399a2985f8e75dad7600c5d89fe3824ffa99ec1c3eb8bf3b0501'),
        pubkey=decode_hex('0xefb86a3594351072c154998f4b635a3f92b3cda96f17011f831f5c2d76bdf1f37c9a00bffc5df70777845d6dee12416c563477d36a432e64cd50836ea1a6cdce'),  # noqa: E501
        sig=decode_hex('0xed7342f0105cff653b6161939d5234b1b100c266871dd6dbf8b4cf9c0cd616ef59065a99f1bf3b28a8136c4fc5495581126f5494b8dde2656bc9b396a1a6764700'),  # noqa: E501
        raw_sig=(
            0,
            107401794514052990211903293686883034296430129698071002460177665452462583453423,
            40267069913801360295276366409101150554378057606663028219514489892367046702663,
        )
    ),
    "bob": dict(
        privkey=decode_hex('0x38e47a7b719dce63662aeaf43440326f551b8a7ee198cee35cb5d517f2d296a2'),
        pubkey=decode_hex('0xfa4f77af824da1f35a166fb4c0287a65555c8068b0563e7754419c4e54e14a0d492592a224590867227ab402dc2ba341ff3cb5207248eecb5782620814ff633f'),  # noqa: E501
        sig=decode_hex('0xf94373aa0d0e85d032619d1b2306615bb7ca57e8ffdd4cde3b7f73db7ff3709a3b8711a4c4b2b832c76aeadabc3e7fde32f62e28ba2a8f296f568ae05286104700'),  # noqa: E501
        raw_sig=(
            0,
            112745076335969330872758377931823342087587667110543084915336202039413408231578,
            26925104191991677765992122469825386008017596401774391204615163577914834161735,
        ),
    ),
    "eve": dict(
        privkey=decode_hex('0x876be0999ed9b7fc26f1b270903ef7b0c35291f89407903270fea611c85f515c'),
        pubkey=decode_hex('0xcfdc6ecb0dd3e4c84e45689c2881fbbed71b3014e09ec380e281e00006a8ff8f53a5ad939af4c19c885bb5cc8a0f0a129d2794b16d4204c84f5445b2eb74e3ac'),  # noqa: E501
        sig=decode_hex('0x68f104b4f5ff8895709e6ba2ae8b30ba7247ce51f15c0eb02df1e41d99e2a89a28977b384b36b17842c245b833ca9c6bf0aec63500904c67b3047cdd815dffa800'),  # noqa: E501
        raw_sig=(
            0,
            47466378880953714119574921231925181230498703786326545694697540952366336092314,
            18360158282590781538070317562901255517896389542202561450761844694916924309416,
        ),
    ),
}


@pytest.fixture(params=['alice', 'bob', 'eve'])
def key_fixture(request):
    if request.param == 'alice':
        return SECRETS['alice']
    elif request.param == 'bob':
        return SECRETS['bob']
    elif request.param == 'eve':
        return SECRETS['eve']
    else:
        assert False, "Should be unreachable"
