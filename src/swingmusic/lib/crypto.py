from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from swingmusic.settings import Paths
from swingmusic.utils.crypto import (
    generate_ed25519_keypair,
    load_private_key_from_file,
    load_public_key_from_hex,
)


class Cryptography:
    """
    This class manages the server's identity, 
    """

    _private_key: ed25519.Ed25519PrivateKey

    @property
    def private_key(self) -> str:
        """
        The loaded private key as hex string.
        """
        return self._private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        ).hex()

    @property
    def public_key(self) -> str:
        """
        The loaded public key as hex string.
        """
        return (
            self._private_key.public_key()
            .public_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PublicFormat.Raw,
            )
            .hex()
        )

    def __init__(self):
        """
        Initialize the Cryptography class.

        Creates a new ed25519 keypair and saves it to the config directory if it doesn't exist.
        """
        private_key_path = Paths().config_dir / "private.key"

        if not private_key_path.exists():
            # Generate new ed25519 keypair
            private_key_hex, _ = generate_ed25519_keypair()
            private_key_path.write_text(private_key_hex)

        self._private_key = load_private_key_from_file(private_key_path)

    def sign(self, message: str) -> str:
        """
        Sign a message using the private key.
        """
        return self._private_key.sign(message.encode("utf-8")).hex()

    @classmethod
    def verify(cls, message: str, signature: str, public_key: str) -> bool:
        """
        Verify a message signature using the public key.
        """
        return load_public_key_from_hex(public_key).verify(
            signature.encode("utf-8"), message.encode("utf-8")
        )
