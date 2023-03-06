import logging, math
from time import sleep
from djitellopy import Tello


class Drone:
    """Represents one instance of tello drone"""

    # Represents the m x n grid that the drone is capable of flying within. Starts at origin.
    BOUNDS = [100, 100]

    def __init__(self):
        self.drone = Tello()

        self.flying = False
        self.location = [0, 0, 0]  # Change location to a map
        self.orientation = 0

        self.drone.connect()

    def validate_location(self, x: int, y: int) -> bool:
        """Validate that target location is within BOUNDS"""

        logging.info(
            f"Validating target location is within bounds [{self.BOUNDS[0]}, {self.BOUNDS[1]}]"
        )

        valid = x >= 0 and y >= 0
        valid &= x <= self.BOUNDS[0] and y <= self.BOUNDS[1]

        return valid

    def initiate_flight(self) -> None:
        assert (
            not self.flying
        ), "ERROR - BAD_COMMAND: Attempting to takeoff when drone already in flight"

        logging.info("Initiating takeoff...")

        self.drone.takeoff()
        self.flying = True

        logging.info("Takeoff completed.")

    def finish_flight(self) -> None:
        assert (
            self.flying
        ), "ERROR - BAD_COMMAND: Attempting to land while drone already grounded"

        logging.info("Initiating landing...")

        self.drone.land()
        self.flying = False

        logging.info("Landing completed.")

    def fly_to_location(self, x: int, y: int) -> None:
        """Make drone fly from current location to target location"""

        assert self.validate_location(
            x, y
        ), "ERROR - BAD_COMMAND: Improper location coordinates supplied"
        assert (
            x != self.location[0] and y != self.location[1]
        ), "ERROR - BAD_COMMAND: Drone already at target location"

        if not self.flying:
            logging.info("Drone not in flight, commencing takeoff...")
            self.drone.takeoff()
            self.flying = True

        # Calculate angle and distance to travel
        delta_x = x - self.location[0]
        delta_y = y = self.location[1]
        if delta_x == 0:
            theta = (
                90 if delta_y > 0 else 270
            )  # If the target location is directly above or below the current location, calculation will fail
        else:
            theta = math.atan(delta_y / delta_x) * (180 / math.pi)
        distance = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))

        logging.info(
            f"Current location [{self.location[0]}, {self.location[1]}] facing {self.orientation} degrees"
        )
        logging.info(f"Need to face {theta} degrees and fly {distance} centimeters")

        # Turn and move
        delta_theta = int(self.orientation - theta)
        if theta < self.orientation:
            logging.info(f"Rotating clockwise {delta_theta} degrees...")
            self.drone.rotate_clockwise(delta_theta)
        elif theta > self.orientation:
            delta_theta *= -1
            logging.info(f"Rotating counter-clockwise {delta_theta} degrees...")
            self.drone.rotate_counter_clockwise(delta_theta)
        logging.info(f"Moving forward {distance} centimeters...")
        self.drone.move_forward(distance)

        self.location[0] = x
        self.location[1] = y
        self.orientation = theta

        logging.info(
            f"Location updated to [{self.location[0]}, {self.location[1]}] facing {self.orientation} degrees"
        )

    def pit_stop(self, duration: int) -> None:
        assert (
            self.flying
        ), "ERROR - BAD_COMMAND: Attempting to land while drone already grounded"

        logging.info(f"Commencing pit stop for {duration} seconds...")

        self.drone.land()
        self.flying = False

        sleep(duration)
        logging.info("Pit stop finished. Commencing takeoff...")

        self.drone.takeoff()
        self.flying = True

    def fly_square_path(self):
        logging.info("Commencing square path demo...")

        stop_duration = 3

        self.initiate_flight()
        self.fly_to_location(0, self.BOUNDS[1])
        self.pit_stop(stop_duration)
        self.fly_to_location(self.BOUNDS[0], self.BOUNDS[1])
        self.pit_stop(stop_duration)
        self.fly_to_location(self.BOUNDS[0], 0)
        self.fly_to_location(0, 0)
        self.finish_flight()
