from typing import Dict, Any

class DriverModel:
    def __init__(self):
        self.drivers: Dict[str, Any] = {}

    def get_driver(self, username: str) -> Any:
        return self.drivers.get(username, None)
    
    def set_driver(self, username: str, driver: Any):
        self.drivers[username] = driver

    def remove_driver(self, username: str):
        self.drivers.pop(username)

driver_model = DriverModel()
