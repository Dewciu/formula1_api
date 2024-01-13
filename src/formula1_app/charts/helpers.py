class GetDriversFullnames:
    def __init__(self, drivers: list[dict[str, str]]):
        self.drivers = drivers

    def get(self) -> list[str]:
        return [
            str(driver["forename"]) + " " + str(driver["surname"])
            for driver in self.drivers
            if driver["forename"] and driver["surname"] is not None
        ]
