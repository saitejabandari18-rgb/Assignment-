class Device:

    def __init__(self, name, room, watts):
        self.name = name
        self.room = room
        self.watts = watts

    def __str__(self):
        return f"{self.name} in {self.room} ({self.watts} W)"

    def __eq__(self, other):
        if not isinstance(other, Device):
            return False

        return self.name == other.name and self.room == other.room

    def daily_kwh(self, hours_on):
        return self.watts * hours_on / 1000


class SmartLamp(Device):

    def __init__(self, name, room, watts, brightness):
        super().__init__(name, room, watts)

        if brightness < 0 or brightness > 100:
            raise ValueError("Brightness must be between 0 and 100")

        self.brightness = brightness

    def __str__(self):
        return (
            f"{self.name} in {self.room} "
            f"({self.watts} W, brightness {self.brightness}%)"
        )

    def dim(self, percent):
        self.brightness = self.brightness - percent

        if self.brightness < 0:
            self.brightness = 0


class House:

    def __init__(self):
        self.devices = []

    def add(self, device):
        if device in self.devices:
            return

        self.devices.append(device)

    def devices_in(self, room):
        result = []

        for device in self.devices:
            if device.room == room:
                result.append(device)

        return result

    def power_hungriest(self):
        if len(self.devices) == 0:
            return None

        highest = self.devices[0]

        for device in self.devices:
            if device.watts > highest.watts:
                highest = device

        return highest

    def __len__(self):
        return len(self.devices)


# Demo
if __name__ == "__main__":

    lamp = Device("Lamp", "living room", 12)
    tv = Device("TV", "living room", 100)
    fridge = Device("Fridge", "kitchen", 150)

    smart_lamp1 = SmartLamp(
        "Smart Lamp 1",
        "bedroom",
        15,
        80
    )

    smart_lamp2 = SmartLamp(
        "Smart Lamp 2",
        "kitchen",
        20,
        60
    )

    house = House()

    house.add(lamp)
    house.add(tv)
    house.add(fridge)
    house.add(smart_lamp1)
    house.add(smart_lamp2)

    # Duplicate device
    duplicate_lamp = Device("Lamp", "living room", 20)
    house.add(duplicate_lamp)

    print("Lamp:", lamp)
    print("Smart lamp:", smart_lamp1)

    print("Lamp == duplicate:", lamp == duplicate_lamp)

    print("Lamp consumption:", lamp.daily_kwh(5), "kWh")

    smart_lamp1.dim(30)
    print("After dimming:", smart_lamp1)

    print("Devices in living room:")

    for device in house.devices_in("living room"):
        print(device)

    print("Power-hungriest:", house.power_hungriest())

    print("Number of devices:", len(house))