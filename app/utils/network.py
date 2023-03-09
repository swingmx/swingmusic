import requests
import socket as Socket


class Ping:
    """
    Checks if there is a connection to the internet by pinging google.com
    """

    @staticmethod
    def __call__() -> bool:
        try:
            requests.get("https://google.com", timeout=10)
            return True
        except (requests.exceptions.ConnectionError, requests.Timeout):
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
