"""
This type stub file was generated by pyright.
"""

import typing
import seleniumwire.thirdparty.mitmproxy.types
from seleniumwire.thirdparty.mitmproxy import command, flow

CONF_DIR = ...
LISTEN_PORT = ...
class Core:
    def load(self, loader): # -> None:
        ...
    
    def configure(self, updated): # -> None:
        ...
    
    @command.command("set")
    def set(self, option: str, value: str = ...) -> None:
        """
            Set an option. When the value is omitted, booleans are set to true,
            strings and integers are set to None (if permitted), and sequences
            are emptied. Boolean values can be true, false or toggle.
            Multiple values are concatenated with a single space.
        """
        ...
    
    @command.command("flow.resume")
    def resume(self, flows: typing.Sequence[flow.Flow]) -> None:
        """
            Resume flows if they are intercepted.
        """
        ...
    
    @command.command("flow.mark")
    def mark(self, flows: typing.Sequence[flow.Flow], boolean: bool) -> None:
        """
            Mark flows.
        """
        ...
    
    @command.command("flow.mark.toggle")
    def mark_toggle(self, flows: typing.Sequence[flow.Flow]) -> None:
        """
            Toggle mark for flows.
        """
        ...
    
    @command.command("flow.kill")
    def kill(self, flows: typing.Sequence[flow.Flow]) -> None:
        """
            Kill running flows.
        """
        ...
    
    @command.command("flow.revert")
    def revert(self, flows: typing.Sequence[flow.Flow]) -> None:
        """
            Revert flow changes.
        """
        ...
    
    @command.command("flow.set.options")
    def flow_set_options(self) -> typing.Sequence[str]:
        ...
    
    @command.command("flow.set")
    @command.argument("attr", type=seleniumwire.thirdparty.mitmproxy.types.Choice("flow.set.options"))
    def flow_set(self, flows: typing.Sequence[flow.Flow], attr: str, value: str) -> None:
        """
            Quickly set a number of common values on flows.
        """
        ...
    
    @command.command("flow.decode")
    def decode(self, flows: typing.Sequence[flow.Flow], part: str) -> None:
        """
            Decode flows.
        """
        ...
    
    @command.command("flow.encode.toggle")
    def encode_toggle(self, flows: typing.Sequence[flow.Flow], part: str) -> None:
        """
            Toggle flow encoding on and off, using deflate for encoding.
        """
        ...
    
    @command.command("flow.encode")
    @command.argument("encoding", type=seleniumwire.thirdparty.mitmproxy.types.Choice("flow.encode.options"))
    def encode(self, flows: typing.Sequence[flow.Flow], part: str, encoding: str) -> None:
        """
            Encode flows with a specified encoding.
        """
        ...
    
    @command.command("flow.encode.options")
    def encode_options(self) -> typing.Sequence[str]:
        """
            The possible values for an encoding specification.
        """
        ...
    
    @command.command("options.load")
    def options_load(self, path: seleniumwire.thirdparty.mitmproxy.types.Path) -> None:
        """
            Load options from a file.
        """
        ...
    
    @command.command("options.save")
    def options_save(self, path: seleniumwire.thirdparty.mitmproxy.types.Path) -> None:
        """
            Save options to a file.
        """
        ...
    
    @command.command("options.reset")
    def options_reset(self) -> None:
        """
            Reset all options to defaults.
        """
        ...
    
    @command.command("options.reset.one")
    def options_reset_one(self, name: str) -> None:
        """
            Reset one option to its default value.
        """
        ...
    


