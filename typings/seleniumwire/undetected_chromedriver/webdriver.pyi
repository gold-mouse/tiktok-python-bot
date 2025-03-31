"""
This type stub file was generated by pyright.
"""

import undetected_chromedriver as uc
from seleniumwire.inspect import InspectRequestsMixin
from seleniumwire.webdriver import DriverCommonMixin

log = ...
class Chrome(InspectRequestsMixin, DriverCommonMixin, uc.Chrome):
    """Extends the undetected_chrome Chrome webdriver to provide additional
    methods for inspecting requests."""
    def __init__(self, *args, seleniumwire_options=..., **kwargs) -> None:
        """Initialise a new Chrome WebDriver instance.

        Args:
            seleniumwire_options: The seleniumwire options dictionary.
        """
        ...
    


ChromeOptions = ...
