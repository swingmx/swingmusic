"""
Cloud API client with Ed25519 request signing for Swing Music Cloud services.
"""

import json
import time
import hashlib
from typing import Any, Literal

import requests

from swingmusic.lib.crypto import Cryptography
from swingmusic.lib.device import get_device_type


class CloudError(Exception):
    """Base exception for cloud API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class CloudAuthError(CloudError):
    """Authentication or authorization error (401/403)."""

    pass


class CloudNetworkError(CloudError):
    """Network connectivity error."""

    pass


class CloudClient:
    """
    HTTP client for Swing Music Cloud API with Ed25519 request signing.

    All requests are signed using the device's Ed25519 private key.
    The signature format is: {timestamp}:{METHOD}:{path}:{sha256(body)}
    """

    # BASE_URL = "http://localhost:1957"
    BASE_URL = "https://cloud.swingmx.com"
    REQUEST_TIMEOUT = 30

    def __init__(self):
        self._crypto = Cryptography()

    def _sha256_hex(self, data: str) -> str:
        """Compute SHA-256 hash of string data, return as hex."""
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def _sign_request(self, method: str, path: str, body: str, timestamp: int) -> str:
        """
        Sign a request using Ed25519.

        Signature message format: {timestamp}:{METHOD}:{path}:{sha256(body)}
        """
        body_hash = self._sha256_hex(body)
        message = f"{timestamp}:{method}:{path}:{body_hash}"
        return self._crypto.sign(message)

    def _make_request(
        self,
        method: Literal["GET", "POST", "PATCH", "DELETE"],
        path: str,
        body: dict[str, Any] | list | None = None,
    ) -> dict[str, Any]:
        """
        Make a signed request to the cloud API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            path: Request path (e.g., /auth/register)
            body: Request body (will be JSON-encoded)

        Returns:
            Parsed JSON response

        Raises:
            CloudAuthError: For 401/403 responses
            CloudNetworkError: For connection errors
            CloudError: For other HTTP errors
        """
        timestamp = int(time.time())
        body_str = json.dumps(body) if body else ""

        signature = self._sign_request(method, path, body_str, timestamp)

        headers = {
            "Content-Type": "application/json",
            "X-Public-Key": self._crypto.public_key,
            "X-Signature": signature,
            "X-Timestamp": str(timestamp),
        }

        url = f"{self.BASE_URL}{path}"

        try:
            if method == "GET":
                response = requests.get(
                    url, headers=headers, timeout=self.REQUEST_TIMEOUT
                )
            elif method == "POST":
                response = requests.post(
                    url, headers=headers, data=body_str, timeout=self.REQUEST_TIMEOUT
                )
            elif method == "PATCH":
                response = requests.patch(
                    url, headers=headers, data=body_str, timeout=self.REQUEST_TIMEOUT
                )
            elif method == "DELETE":
                response = requests.delete(
                    url, headers=headers, timeout=self.REQUEST_TIMEOUT
                )

        except requests.exceptions.ConnectionError as e:
            raise CloudNetworkError(f"Failed to connect to cloud server: {e}")
        except (requests.exceptions.Timeout, requests.exceptions.ReadTimeout) as e:
            raise CloudNetworkError(f"Request timed out: {e}")
        except requests.exceptions.RequestException as e:
            raise CloudNetworkError(f"Request failed: {e}")


        # Handle response
        if response.status_code == 200:
            try:
                return response.json()
            except json.JSONDecodeError:
                return response.content

        # Parse error message
        try:
            error_data = response.json()
            error_msg = error_data.get("error", response.text)
        except (json.JSONDecodeError, ValueError):
            error_msg = response.text

        if response.status_code in (401, 403):
            raise CloudAuthError(error_msg, status_code=response.status_code)

        if response.status_code == 429:
            raise CloudError("Rate limit exceeded", status_code=429)

        raise CloudError(error_msg, status_code=response.status_code)

    def register(
        self, license_key: str, device_id: str, device_name: str
    ) -> dict[str, Any]:
        """
        Register a device with a license key.

        POST /auth/register

        Args:
            license_key: Valid Polar.sh license key
            device_id: 16-character hex hardware identifier
            device_name: Human-readable device name (1-50 chars)

        Returns:
            Registration response with user, customer, and devices info

        Raises:
            CloudAuthError: Invalid license or signature
            CloudError: Other registration errors
        """
        return self._make_request(
            "POST",
            "/auth/register",
            {
                "license_key": license_key,
                "device_id": device_id,
                "device_name": device_name,
                "device_type": get_device_type(),
            },
        )

    def get_auth_status(self) -> dict[str, Any]:
        """
        Get current authentication status.

        GET /auth/status

        Returns:
            Status response with user and devices info

        Raises:
            CloudAuthError: User not registered or expired
        """
        return self._make_request("GET", "/auth/status")

    def update_device_name(self, device_name: str) -> dict[str, Any]:
        """
        Update the current device's name.

        PATCH /auth/device

        Args:
            device_name: New device name (1-50 chars)

        Returns:
            Updated device info
        """
        return self._make_request(
            "PATCH",
            "/auth/device",
            {"device_name": device_name},
        )

    def revoke_device(self, device_id: str) -> dict[str, Any]:
        """
        Revoke a device from the license.

        DELETE /auth/device/{device_id}

        Args:
            device_id: 16-character hex ID of device to revoke

        Returns:
            Revocation result with updated device count
        """
        return self._make_request("DELETE", f"/auth/device/{device_id}")
