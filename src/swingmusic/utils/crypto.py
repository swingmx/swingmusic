"""
Cryptographic utilities for server identity and key management.
"""

from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


def generate_ed25519_keypair() -> tuple[str, str]:
    """
    Generate a new ed25519 key pair.

    Returns:
        tuple[str, str]: (private_key_hex, public_key_hex)
    """
    # Generate ed25519 keypair
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    # Convert to hex format
    private_hex = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption(),
    ).hex()

    public_hex = public_key.public_bytes(
        encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
    ).hex()

    return private_hex, public_hex


def load_private_key_from_hex(private_hex: str) -> ed25519.Ed25519PrivateKey:
    """
    Load an ed25519 private key from hex string.

    Args:
        private_hex: 64-character hex string representing the private key

    Returns:
        ed25519.Ed25519PrivateKey: The loaded private key object
    """
    private_bytes = bytes.fromhex(private_hex)
    return ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)


def load_public_key_from_hex(public_hex: str) -> ed25519.Ed25519PublicKey:
    """
    Load an ed25519 public key from hex string.

    Args:
        public_hex: 64-character hex string representing the public key

    Returns:
        ed25519.Ed25519PublicKey: The loaded public key object
    """
    public_bytes = bytes.fromhex(public_hex)
    return ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)


def load_private_key_from_file(private_key_path: Path) -> ed25519.Ed25519PrivateKey:
    """
    Load an ed25519 private key from a file containing hex-encoded key.

    Args:
        private_key_path: Path to the private key file

    Returns:
        ed25519.Ed25519PrivateKey: The loaded private key object

    Raises:
        FileNotFoundError: If the private key file doesn't exist
        ValueError: If the file doesn't contain a valid hex-encoded key
    """
    if not private_key_path.exists():
        raise FileNotFoundError(f"Private key file not found: {private_key_path}")

    private_hex = private_key_path.read_text().strip()

    if len(private_hex) != 64:
        raise ValueError(
            f"Invalid private key length: expected 64 hex characters, got {len(private_hex)}"
        )

    return load_private_key_from_hex(private_hex)
