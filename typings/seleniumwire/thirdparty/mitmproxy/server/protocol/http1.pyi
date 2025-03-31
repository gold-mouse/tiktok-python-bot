"""
This type stub file was generated by pyright.
"""

from seleniumwire.thirdparty.mitmproxy.server.protocol import http as httpbase

class Http1Layer(httpbase._HttpTransmissionLayer):
    def __init__(self, ctx, mode) -> None:
        ...
    
    def read_request_headers(self, flow): # -> Request:
        ...
    
    def read_request_body(self, request): # -> Generator[Any, Any, None]:
        ...
    
    def read_request_trailers(self, request): # -> None:
        ...
    
    def send_request_headers(self, request): # -> None:
        ...
    
    def send_request_body(self, request, chunks): # -> None:
        ...
    
    def send_request_trailers(self, request): # -> None:
        ...
    
    def send_request(self, request): # -> None:
        ...
    
    def read_response_headers(self): # -> Response:
        ...
    
    def read_response_body(self, request, response): # -> Generator[Any, Any, None]:
        ...
    
    def read_response_trailers(self, request, response): # -> None:
        ...
    
    def send_response_headers(self, response): # -> None:
        ...
    
    def send_response_body(self, response, chunks): # -> None:
        ...
    
    def send_response_trailers(self, response): # -> None:
        ...
    
    def check_close_connection(self, flow): # -> bool:
        ...
    
    def __call__(self): # -> None:
        ...
    


