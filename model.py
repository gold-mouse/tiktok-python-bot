from typing import Dict, Any, List

class DriverModel:
    def __init__(self):
        self.drivers: Dict[str, Any] = {}
        self.offsets: Dict[str, Any] = {}
        self.pids: Dict[str, Any] = {}

    def get_chrome_pid(self, username: str):
        if self.drivers[username] == None:
            return None
        return self.drivers[username].service.process.pid

    def get_driver(self, username: str) -> Any:
        return self.drivers.get(username, None)
    
    def set_driver(self, username: str, driver: Any):
        # Set driver
        self.drivers[username] = driver

        # Set browser offset
        viewport_height = driver.execute_script("return window.innerHeight") # Get viewport height
        full_window_height = driver.execute_script("return window.outerHeight") # Get full window height
        browser_offset = full_window_height - viewport_height

        self.offsets[username] = browser_offset

        # Set pid
        pid = self.get_chrome_pid(username)

        self.pids[username] = pid or "Not Found Pid"

    def remove_driver(self, username: str):
        self.drivers.pop(username)
        self.offsets.pop(username)
        self.pids.pop(username)

    def get_browser_offset(self, username: str):
        return self.offsets.get(username, 0)

    def get_pid(self, username: str):
        return self.pids.get(username, None)

    def get_keys(self) -> List[str]:
        allkeys = self.drivers.keys()
        return list(allkeys)

driver_model = DriverModel()
