import socket as Socket


def has_connection(host="google.it", port=80, timeout=3):
    """
    # REVIEW Was:
    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        Socket.setdefaulttimeout(timeout)
        Socket.socket(Socket.AF_INET, Socket.SOCK_STREAM).connect((host, port))
        return True
    except Socket.error as ex:
        return False


def get_ip():
    """
    Get the IP address of the current system.
    Will return address of default outgoing chanel.
    """
    soc = Socket.socket(Socket.AF_INET, Socket.SOCK_DGRAM)
    try:
        soc.connect(("8.8.8.8", 80))
    except OSError:
        return None
    ip_address = str(soc.getsockname()[0])
    soc.close()

    return ip_address
