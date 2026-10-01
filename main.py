from datetime import datetime


# ============================================================
# DECORATORS
# ============================================================

def log_operation(func):
    """Decorator to log parking operations."""

    def wrapper(*args, **kwargs):

        print(f"\n[LOG] Operation started: {func.__name__}")

        result = func(*args, **kwargs)

        print(
            f"[LOG] Operation completed at "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )

        return result

    return wrapper


def validate_vehicle(func):
    """Decorator to check whether a vehicle is parked."""

    def wrapper(self, vehicle_number, *args, **kwargs):

        if vehicle_number not in self.parked_vehicles:

            print(
                f"Vehicle '{vehicle_number}' "
                f"is not currently parked."
            )

            return

        return func(
            self,
            vehicle_number,
            *args,
            **kwargs
        )

    return wrapper


# ============================================================
# VEHICLE CLASS
# ============================================================

class Vehicle:

    def __init__(self, vehicle_number, owner_name):

        self.vehicle_number = vehicle_number
        self.owner_name = owner_name
        self.entry_time = datetime.now()

    def calculate_charge(self, hours):

        return hours * 20

    def __str__(self):

        return (
            f"Vehicle: {self.vehicle_number} | "
            f"Owner: {self.owner_name}"
        )


# ============================================================
# CAR CLASS
# ============================================================

class Car(Vehicle):

    def calculate_charge(self, hours):

        return hours * 30

    def __str__(self):

        return (
            f"[CAR] "
            f"Vehicle: {self.vehicle_number} | "
            f"Owner: {self.owner_name}"
        )


# ============================================================
# BIKE CLASS
# ============================================================

class Bike(Vehicle):

    def calculate_charge(self, hours):

        return hours * 10

    def __str__(self):

        return (
            f"[BIKE] "
            f"Vehicle: {self.vehicle_number} | "
            f"Owner: {self.owner_name}"
        )


# ============================================================
# TRUCK CLASS
# ============================================================

class Truck(Vehicle):

    def calculate_charge(self, hours):

        return hours * 50

    def __str__(self):

        return (
            f"[TRUCK] "
            f"Vehicle: {self.vehicle_number} | "
            f"Owner: {self.owner_name}"
        )


# ============================================================
# PARKING LOT CLASS
# ============================================================

class ParkingLot:

    def __init__(self, total_spaces):

        self.total_spaces = total_spaces

        # vehicle_number -> Vehicle object
        self.parked_vehicles = {}

    # --------------------------------------------------------
    # PARK VEHICLE
    # --------------------------------------------------------

    @log_operation
    def park_vehicle(
        self,
        vehicle_type,
        vehicle_number,
        owner_name
    ):

        if vehicle_number in self.parked_vehicles:

            print(
                "This vehicle is already parked."
            )

            return

        if len(self.parked_vehicles) >= self.total_spaces:

            print(
                "Parking lot is full."
            )

            return

        if vehicle_type.lower() == "car":

            vehicle = Car(
                vehicle_number,
                owner_name
            )

        elif vehicle_type.lower() == "bike":

            vehicle = Bike(
                vehicle_number,
                owner_name
            )

        elif vehicle_type.lower() == "truck":

            vehicle = Truck(
                vehicle_number,
                owner_name
            )

        else:

            print(
                "Invalid vehicle type."
            )

            return

        self.parked_vehicles[
            vehicle_number
        ] = vehicle

        print(
            f"Vehicle {vehicle_number} "
            f"parked successfully."
        )

    # --------------------------------------------------------
    # REMOVE VEHICLE
    # --------------------------------------------------------

    @log_operation
    @validate_vehicle
    def remove_vehicle(
        self,
        vehicle_number
    ):

        vehicle = self.parked_vehicles[
            vehicle_number
        ]

        # Ask user for parking duration
        try:

            hours = float(
                input(
                    "Enter parking duration "
                    "(in hours): "
                )
            )

        except ValueError:

            print(
                "Invalid duration."
            )

            return

        if hours <= 0:

            print(
                "Duration must be greater than 0."
            )

            return

        charge = vehicle.calculate_charge(
            hours
        )

        del self.parked_vehicles[
            vehicle_number
        ]

        print(
            f"\nVehicle: {vehicle_number}"
        )

        print(
            f"Parking Duration: {hours} hours"
        )

        print(
            f"Parking Charge: ₹{charge:.2f}"
        )

        print(
            "Vehicle removed successfully."
        )

    # --------------------------------------------------------
    # SEARCH VEHICLE
    # --------------------------------------------------------

    def search_vehicle(
        self,
        vehicle_number
    ):

        if vehicle_number not in self.parked_vehicles:

            print(
                "Vehicle not found."
            )

            return

        vehicle = self.parked_vehicles[
            vehicle_number
        ]

        print(
            "\nVehicle Found:"
        )

        print(vehicle)

        print(
            f"Entry Time: "
            f"{vehicle.entry_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    # --------------------------------------------------------
    # DISPLAY ALL VEHICLES
    # --------------------------------------------------------

    def display_vehicles(self):

        if not self.parked_vehicles:

            print(
                "\nNo vehicles are currently parked."
            )

            return

        print(
            "\n========== PARKED VEHICLES =========="
        )

        for vehicle in self.parked_vehicles.values():

            print(vehicle)

            print(
                f"Entry Time: "
                f"{vehicle.entry_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

            print("-" * 50)

    # --------------------------------------------------------
    # DISPLAY PARKING STATUS
    # --------------------------------------------------------

    def parking_status(self):

        occupied = len(
            self.parked_vehicles
        )

        available = (
            self.total_spaces - occupied
        )

        print(
            "\n========== PARKING STATUS =========="
        )

        print(
            f"Total Spaces     : {self.total_spaces}"
        )

        print(
            f"Occupied Spaces  : {occupied}"
        )

        print(
            f"Available Spaces : {available}"
        )


# ============================================================
# INPUT FUNCTIONS
# ============================================================

def get_vehicle_number():

    vehicle_number = input(
        "Enter vehicle number: "
    ).strip().upper()

    if not vehicle_number:

        print(
            "Vehicle number cannot be empty."
        )

        return None

    return vehicle_number


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    parking_lot = ParkingLot(
        total_spaces=5
    )

    while True:

        print("\n")
        print("=" * 55)
        print("        SMART PARKING MANAGEMENT SYSTEM")
        print("=" * 55)

        print("1. Park Vehicle")
        print("2. Remove Vehicle")
        print("3. Search Vehicle")
        print("4. Display Parked Vehicles")
        print("5. Parking Status")
        print("6. Exit")

        print("=" * 55)

        choice = input(
            "Enter your choice: "
        )

        # ----------------------------------------------------
        # PARK VEHICLE
        # ----------------------------------------------------

        if choice == "1":

            print(
                "\nVehicle Types:"
            )

            print("1. Car")
            print("2. Bike")
            print("3. Truck")

            vehicle_choice = input(
                "Select vehicle type: "
            )

            if vehicle_choice == "1":

                vehicle_type = "car"

            elif vehicle_choice == "2":

                vehicle_type = "bike"

            elif vehicle_choice == "3":

                vehicle_type = "truck"

            else:

                print(
                    "Invalid vehicle type."
                )

                continue

            vehicle_number = get_vehicle_number()

            if vehicle_number is None:

                continue

            owner_name = input(
                "Enter owner name: "
            )

            parking_lot.park_vehicle(
                vehicle_type,
                vehicle_number,
                owner_name
            )

        # ----------------------------------------------------
        # REMOVE VEHICLE
        # ----------------------------------------------------

        elif choice == "2":

            vehicle_number = get_vehicle_number()

            if vehicle_number is not None:

                parking_lot.remove_vehicle(
                    vehicle_number
                )

        # ----------------------------------------------------
        # SEARCH VEHICLE
        # ----------------------------------------------------

        elif choice == "3":

            vehicle_number = get_vehicle_number()

            if vehicle_number is not None:

                parking_lot.search_vehicle(
                    vehicle_number
                )

        # ----------------------------------------------------
        # DISPLAY VEHICLES
        # ----------------------------------------------------

        elif choice == "4":

            parking_lot.display_vehicles()

        # ----------------------------------------------------
        # PARKING STATUS
        # ----------------------------------------------------

        elif choice == "5":

            parking_lot.parking_status()

        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        elif choice == "6":

            print(
                "\nThank you for using "
                "Smart Parking Management System!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please try again."
            )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
