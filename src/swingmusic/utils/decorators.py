from functools import wraps


def coroutine(func):
    """
    Decorator: primes `func` by advancing to first `yield`
    """

    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start


def license_required(func):
    """
    Decorator that ensures the user has a valid license.

    Raises LicenseError if not licensed. The caller should handle:
    - LicenseNotFoundError: No license configured or not activated
    - LicenseExpiredError: License has expired
    - LicenseRevokedError: Device was revoked
    - LicenseValidationError: Grace period exceeded

    Usage:
        @license_required
        def premium_feature():
            # Only runs if licensed
            ...

        # Caller handles:
        try:
            premium_feature()
        except LicenseError as e:
            show_upgrade_prompt(str(e))
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # Import here to avoid circular imports
        from swingmusic.lib.license import LicenseManager

        LicenseManager().check_license()  # Raises on failure
        return func(*args, **kwargs)

    return wrapper
