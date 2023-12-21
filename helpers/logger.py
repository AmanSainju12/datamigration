import logging


class Logger:
    def __init__(self):
        # Configure the logging
        self.log_filename = 'test.log'
        logging.basicConfig(filename=self.log_filename, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def write_log(message, log_level):
        match log_level:
            case "error":
                logging.error(message)
            case "warning":
                logging.warning(message)
            case "critical":
                logging.critical(message)
            case "info":
                logging.info(message)
