"""
This type stub file was generated by pyright.
"""

class LogEntry:
    def __init__(self, msg, level) -> None:
        ...
    
    def __eq__(self, other) -> bool:
        ...
    
    def __repr__(self): # -> LiteralString:
        ...
    


class Log:
    """
        The central logger, exposed to scripts as mitmproxy.ctx.log.
    """
    def __init__(self, master) -> None:
        ...
    
    def debug(self, txt): # -> None:
        """
            Log with level debug.
        """
        ...
    
    def info(self, txt): # -> None:
        """
            Log with level info.
        """
        ...
    
    def alert(self, txt): # -> None:
        """
            Log with level alert. Alerts have the same urgency as info, but
            signals to interactive tools that the user's attention should be
            drawn to the output even if they're not currently looking at the
            event log.
        """
        ...
    
    def warn(self, txt): # -> None:
        """
            Log with level warn.
        """
        ...
    
    def error(self, txt): # -> None:
        """
            Log with level error.
        """
        ...
    
    def __call__(self, text, level=...): # -> None:
        ...
    


LogTierOrder = ...
def log_tier(level): # -> int | None:
    ...

