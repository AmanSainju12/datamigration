from helpers.logger import Logger
from start_up.program import Program


def main():
    Logger.write_log("Program Started", "info")
    # creating instance for Program
    program = Program()
    is_completed = program.file_upload()
    if is_completed:
        Logger.write_log("Program execution completed successfully", "info")
    else:
        Logger.write_log("Program execution couldn't be completed", "error")


if __name__ == "__main__":
    main()
