import logging, sys
from src import basic_path
from os import path, mkdir, listdir


def logfile_setup() -> str:
    """Generate path to logfile."""

    if not path.isdir("logs"):
        mkdir("logs")
    filename = f"log-{len(listdir('logs'))}.log"

    return path.join("logs", filename)


def logger_setup() -> logging.Logger:
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)

    fileHandler = logging.FileHandler(logfile_setup())
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)


def main() -> None:
    drone = basic_path.Drone()

    logging.info("Commencing test flight...")
    drone.fly_square_path()
    logging.info("Test flight ended.")

    sys.exit(0)


if __name__ == "__main__":
    logger_setup()
    main()
