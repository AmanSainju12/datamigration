from helpers.logger import Logger
from start_up.program import Program


def main():
    Logger()
    Logger.write_log("Program Started", "info")
    # creating instance for Program
    try:
        program = Program()
        is_completed = program.file_upload()
        if is_completed:
            Logger.write_log("Program execution completed successfully", "info")
        else:
            Logger.write_log("Program execution couldn't be completed", "error")
    except KeyboardInterrupt:
        Logger.write_log("Program Terminated", "error")
        Logger.write_log("Program execution couldn't be completed", "error")
    except Exception as e:
        Logger.write_log(f"{e}", "error")
        Logger.write_log("Program execution couldn't be completed", "error")


if __name__ == "__main__":
    main()
