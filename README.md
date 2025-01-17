# NewChain Keys


A common API for NewChain key operations with pluggable backends.


> This library and repository is original forked from https://github.com/ethereum/eth-keys.

## Installation

```sh
pip install newchain-keys
```

## Development

```sh
pip install -e .[dev]
```


### Running the tests

You can run the tests with:

```sh
py.test tests
```

Or you can install `tox` to run the full test suite.


### Releasing

Pandoc is required for transforming the markdown README to the proper format to
render correctly on pypi.

For Debian-like systems:

```
apt install pandoc
```

Or on OSX:

```sh
brew install pandoc
```

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```


#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`.

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 2.0.0-alpha.1 devnum"`



## QuickStart

```python
>>> from newchain_keys import keys
>>> pk = keys.PrivateKey(b'\x01' * 32)
>>> signature = pk.sign_msg(b'a message')
>>> pk
'0x0101010101010101010101010101010101010101010101010101010101010101'
>>> pk.public_key
'0x6ff03b949241ce1dadd43519e6960e0a85b41a69a05c328103aa2bce1594ca163c4f753a55bf01dc53f6c0b0c7eee78b40c6ff7d25a96e2282b989cef71c144a'
>>> signature
'0xf5a024b434c72877e7cd4c1f086896477babb10153ef2a787c9276763e6dad1d17d5dcc2a5a611d77e22b06832d84ba6560b0ae36013710156715ea92244fd8901'
>>> pk.public_key.to_checksum_address()
'0xa0E0162b1a12Ed06d63DD1BF0CD5b0d1e6614B3c'
>>> signature.verify_msg(b'a message', pk.public_key)
True
>>> signature.recover_public_key_from_msg(b'a message') == pk.public_key
True
```


## Documentation

### `KeyAPI(backend=None)`

The `KeyAPI` object is the primary API for interacting with the `newchain-keys`
libary.  The object takes a single optional argument in its constructor which
designates what backend will be used for eliptical curve cryptography
operations.  The built-in backends are:

* `newchain_keys.backends.NativeECCBackend`: A pure python implementation of the ECC operations.

By default, `newchain-keys` will *try* to use the `NativeECCBackend`.

The `backend` argument can be given in any of the following forms.

* Instance of the backend class
* The backend class
* String with the dot-separated import path for the backend class.

```python
>>> from newchain_keys import KeyAPI
>>> from newchain_keys.backends import NativeECCBackend
# These are all the same
>>> keys = KeyAPI(NativeECCBackend)
>>> keys = KeyAPI(NativeECCBackend())
>>> keys = KeyAPI('newchain_keys.backends.NativeECCBackend')
```

The backend can also be configured using the environment variable
`ECC_BACKEND_CLASS` which should be set to the dot-separated python import path
to the desired backend.

### `KeyAPI.ecdsa_sign(message_hash, private_key) -> Signature`

This method returns a signature for the given `message_hash`, signed by the
provided `private_key`.

* `message_hash`: **must** be a byte string of length 32
* `private_key`: **must** be an instance of `PrivateKey`


### `KeyAPI.ecdsa_verify(message_hash, signature, public_key) -> bool`

Returns `True` or `False` based on whether the provided `signature` is a valid
signature for the provided `message_hash` and `public_key`.

* `message_hash`: **must** be a byte string of length 32
* `signature`: **must** be an instance of `Signature`
* `public_key`: **must** be an instance of `PublicKey`


### `KeyAPI.ecdsa_recover(message_hash, signature) -> PublicKey`

Returns the `PublicKey` instances recovered from the given `signature` and
`message_hash`.

* `message_hash`: **must** be a byte string of length 32
* `signature`: **must** be an instance of `Signature`


### `KeyAPI.private_key_to_public_key(private_key) -> PublicKey`

Returns the `PublicKey` instances computed from the given `private_key`
instance.

* `private_key`: **must** be an instance of `PublicKey`


### Common APIs for `PublicKey`, `PrivateKey` and `Signature`

There is a common API for the following objects.

* `PublicKey`
* `PrivateKey`
* `Signature`

Each of these objects has all of the following APIs.

* `obj.to_bytes()`: Returns the object in it's canonical `bytes` serialization.
* `obj.to_hex()`: Returns a text string of the hex encoded canonical representation.


### `KeyAPI.PublicKey(public_key_bytes)`

The `PublicKey` class takes a single argument which must be a bytes string with length 64.

> Note that there are two other common formats for public keys: 65 bytes with a leading `\x04` byte
> and 33 bytes starting with either `\x02` or `\x03`. To use the former with the `PublicKey` object,
> remove the first byte. For the latter, refer to `PublicKey.from_compressed_bytes`.

The following methods are available:


#### `PublicKey.from_compressed_bytes(compressed_bytes) -> PublicKey`

This `classmethod` returns a new `PublicKey` instance computed from its compressed representation.

* `compressed_bytes` **must** be a byte string of length 33 starting with `\x02` or `\x03`.


#### `PublicKey.from_private(private_key) -> PublicKey`

This `classmethod` returns a new `PublicKey` instance computed from the
given `private_key`.  

* `private_key` may either be a byte string of length 32 or an instance of the `KeyAPI.PrivateKey` class.


#### `PublicKey.recover_from_msg(message, signature) -> PublicKey`

This `classmethod` returns a new `PublicKey` instance computed from the
provided `message` and `signature`.

* `message` **must** be a byte string
* `signature` **must** be an instance of `KeyAPI.Signature`


#### `PublicKey.recover_from_msg_hash(message_hash, signature) -> PublicKey`

Same as `PublicKey.recover_from_msg` except that `message_hash` should be the Keccak
hash of the `message`.


#### `PublicKey.verify_msg(message, signature) -> bool`

This method returns `True` or `False` based on whether the signature is a valid
for the given message.


#### `PublicKey.verify_msg_hash(message_hash, signature) -> bool`

Same as `PublicKey.verify_msg` except that `message_hash` should be the Keccak
hash of the `message`.


#### `PublicKey.to_compressed_bytes() -> bytes`

Returns the compressed representation of this public key.


#### `PublicKey.to_address() -> text`

Returns the hex encoded ethereum address for this public key.


#### `PublicKey.to_checksum_address() -> text`

Returns the ERC55 checksum formatted ethereum address for this public key.


#### `PublicKey.to_canonical_address() -> bytes`

Returns the 20-byte representation of the ethereum address for this public key.


### `KeyAPI.PrivateKey(private_key_bytes)`

The `PrivateKey` class takes a single argument which must be a bytes string with length 32.

The following methods and properties are available


#### `PrivateKey.public_key`

This *property* holds the `PublicKey` instance coresponding to this private key.


#### `PrivateKey.sign_msg(message) -> Signature`

This method returns a signature for the given `message` in the form of a
`Signature` instance

* `message` **must** be a byte string.


#### `PrivateKey.sign_msg_hash(message_hash) -> Signature`

Same as `PrivateKey.sign` except that `message_hash` should be the Keccak
hash of the `message`.


### `KeyAPI.Signature(signature_bytes=None, vrs=None)`

The `Signature` class can be instantiated in one of two ways.

* `signature_bytes`: a bytes string with length 65.
* `vrs`: a 3-tuple composed of the integers `v`, `r`, and `s`.

> Note: If using the `signature_bytes` to instantiate, the byte string should be encoded as `r_bytes | s_bytes | v_bytes` where `|` represents concatenation.  `r_bytes` and `s_bytes` should be 32 bytes in length.  `v_bytes` should be a single byte `\x00` or `\x01`.

Signatures are expected to use `1` or `0` for their `v` value.

The following methods and properties are available


#### `Signature.v`

This property returns the `v` value from the signature as an integer.


#### `Signature.r`

This property returns the `r` value from the signature as an integer.


#### `Signature.s`

This property returns the `s` value from the signature as an integer.


#### `Signature.vrs`

This property returns a 3-tuple of `(v, r, s)`.


#### `Signature.verify_msg(message, public_key) -> bool`

This method returns `True` or `False` based on whether the signature is a valid
for the given public key.

* `message`: **must** be a byte string.
* `public_key`: **must** be an instance of `PublicKey`


#### `Signature.verify_msg_hash(message_hash, public_key) -> bool`

Same as `Signature.verify_msg` except that `message_hash` should be the Keccak
hash of the `message`.


#### `Signature.recover_public_key_from_msg(message) -> PublicKey`

This method returns a `PublicKey` instance recovered from the signature.

* `message`: **must** be a byte string.


#### `Signature.recover_public_key_from_msg_hash(message_hash) -> PublicKey`

Same as `Signature.recover_public_key_from_msg` except that `message_hash`
should be the Keccak hash of the `message`.


### Exceptions

#### `eth_api.exceptions.ValidationError`

This error is raised during instantaition of any of the `PublicKey`,
`PrivateKey` or `Signature` classes if their constructor parameters are
invalid.


#### `eth_api.exceptions.BadSignature`

This error is raised from any of the `recover` or `verify` methods involving
signatures if the signature is invalid.
