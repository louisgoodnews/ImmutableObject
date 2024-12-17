from logger.logger import Logger


def debug() -> None:
    logger: Logger = Logger.get_logger(name="debug")

    logger.info(message="Hello, World!")


if __name__ == "__main__":
    debug()
