from typing import Dict, Any, List
class DriverModel:
    def __init__(self):
        self.drivers: Dict[str, Any] = {}
        self.solvers: Dict[str, Any] = {}

    def get_driver(self, username: str) -> Any:
        return self.drivers.get(username, None)
    
    def set_driver(self, username: str, driver: Any):
        # Set driver
        self.drivers[username] = driver


    def remove_driver(self, username: str):
        driver = self.drivers.pop(username)
        driver.quit()
        
    def check_driver(self, username: str) -> bool:
        return username in self.drivers

    def get_usernames_from_driverkyes(self) -> List[str]:
        allkeys = self.drivers.keys()
        return list(allkeys)

driver_model = DriverModel()
