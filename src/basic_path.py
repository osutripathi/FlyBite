import logging, math
from djitellopy import Tello


class Drone:
    """Represents one instance of tello drone"""

    #Represents the m x n grid that the drone is capable of flying within. Starts at origin.
    BOUNDS = [100, 100]

    def __init__(self):
        self.drone = Tello()

        self.flying = False
        self.location = [0, 0, 0]   #Change location to a map
        self.orientation = 0
    
    def validate_location(self, x: int, y: int) -> bool:
        """Validate that target location is within BOUNDS"""

        logging.info(f"Validating target location is within bounds [{self.BOUNDS[0]}, {self.BOUNDS[1]}]")

        valid = x >= 0 and y >= 0
        valid = x <= self.BOUNDS[0] and y <= self.BOUNDS[1]

        return valid

    def fly_to_location(self, x: int, y: int) -> None:
        """Make drone fly from current location to target location"""
        assert self.validate_location(x, y)
        assert x != self.location[0] and y != self.location[1]

        if not self.flying:
            logging.info("Drone not in flight, commencing takeoff...")
            self.drone.takeoff()
            self.flying = True
        
        #Calculate angle and distance to travel
        delta_x = x - self.location[0]
        delta_y = y = self.location[1]
        if delta_x == 0:
            theta = 90 if delta_y > 0 else 270  #If the target location is directly above or below the current location, calculation will fail
        else:
            theta = math.atan(delta_y / delta_x) * (180 / math.pi)
        distance = math.sqrt(math.pow(delta_x, 2) + math.pow(delta_y, 2))

        logging.info(f"Current location [{self.location[0]}, {self.location[1]}] facing {self.orientation} degrees")
        logging.info(f"Need to face {theta} degrees and fly {distance} cm")

        #Turn and move
        delta_theta = int(self.orientation - theta)
        if theta < self.orientation:
            logging.info(f"Rotating clockwise {delta_theta} degrees...")
            self.drone.rotate_clockwise(delta_theta)
        elif theta > self.orientation:
            delta_theta *= -1
            logging.info(f"Rotating counter-clockwise {delta_theta} degrees...")
            self.drone.rotate_counter_clockwise(delta_theta)
        logging.info(f"Moving forward {distance} cm...")
        self.drone.move_forward(distance)

        self.location[0] = x
        self.location[1] = y
        self.orientation = theta

        logging.info(f"Location updated to [{self.location[0]}, {self.location[1]}] facing {self.orientation} degrees")