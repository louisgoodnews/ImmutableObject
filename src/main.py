from logger.logger import Logger


def main() -> None:
    logger: Logger = Logger.get_logger(name="main")

    logger.info(message="Hello, World!")


if __name__ == "__main__":
    main()
