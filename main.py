from helpers.logger import Logger
from start_up.program import Program

# creating instance for logger
logger = Logger()


def main():
    logger.write_log("Program Started", "info")
    # creating instance for Program
    program = Program()
    is_completed = program.file_upload()
    if is_completed:
        logger.write_log("Program execution completed successfully", "info")
    else:
        logger.write_log("Program execution couldn't be completed", "error")


if __name__ == "__main__":
    main()
