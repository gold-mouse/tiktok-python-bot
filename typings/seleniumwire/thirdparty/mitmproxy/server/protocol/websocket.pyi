"""
This type stub file was generated by pyright.
"""

from seleniumwire.thirdparty.mitmproxy.server.protocol import base

class WebSocketLayer(base.Layer):
    """
        WebSocket layer to intercept, modify, and forward WebSocket messages.

        Only version 13 is supported (as specified in RFC6455).
        Only HTTP/1.1-initiated connections are supported.

        The client starts by sending an Upgrade-request.
        In order to determine the handshake and negotiate the correct protocol
        and extensions, the Upgrade-request is forwarded to the server.
        The response from the server is then parsed and negotiated settings are extracted.
        Finally the handshake is completed by forwarding the server-response to the client.
        After that, only WebSocket frames are exchanged.

        PING/PONG frames pass through and must be answered by the other endpoint.

        CLOSE frames are forwarded before this WebSocketLayer terminates.

        This layer is transparent to any negotiated extensions.
        This layer is transparent to any negotiated subprotocols.
        Only raw frames are forwarded to the other endpoint.

        WebSocket messages are stored in a WebSocketFlow.
    """
    def __init__(self, ctx, handshake_flow) -> None:
        ...
    
    def __call__(self): # -> None:
        ...
    


