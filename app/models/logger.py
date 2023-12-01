from attr import dataclass


@dataclass 
class Track:
    """
    Track play logger model
    """
    trackhash: str
    duration: int
    timestamp: int