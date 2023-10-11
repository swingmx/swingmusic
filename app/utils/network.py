import socket as Socket


def has_connection(host="8.8.8.8", port=53, timeout=3):
    """
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
    Returns the IP address of this device.
    """
    soc = Socket.socket(Socket.AF_INET, Socket.SOCK_DGRAM)
    soc.connect(("8.8.8.8", 80))
    ip_address = str(soc.getsockname()[0])
    soc.close()

    return ip_address
