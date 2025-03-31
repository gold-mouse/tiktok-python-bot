"""
This type stub file was generated by pyright.
"""

class Masker:
    """
    Data sent from the server must be masked to prevent malicious clients
    from sending data over the wire in predictable patterns.

    Servers do not have to mask data they send to the client.
    https://tools.ietf.org/html/rfc6455#section-5.3
    """
    def __init__(self, key) -> None:
        ...
    
    def mask(self, offset, data): # -> bytes:
        ...
    
    def __call__(self, data): # -> bytes:
        ...
    


