import logging
import os


class Logger:
    """
    Класс логгера

    На данный момент в зачаточном состоянии, умеет приблизительно ничего интересного (и не используется)
    """

    def __init__(self, name=__name__, level=logging.INFO, log_file='logs/app.log', add_console_logs=False):

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        if not self.logger.handlers:
            formatter = Formatter()

            # Консольный обработчик
            if add_console_logs:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                console_handler.setFormatter(formatter)
                self.logger.addHandler(console_handler)

            # Файловый обработчик
            if log_file:
                log_dir = os.path.dirname(log_file)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)


    def info(self, message):
        self.logger.info(message)


    def warning(self, message):
        self.logger.warning(message)


    def error(self, message):
        self.logger.error(message)


    def debug(self, message):
        self.logger.debug(message)


class Formatter(logging.Formatter):
    """
    Класс кастомного форматера

    Умеет преобразовывать сообщение из логгера в красивый вид
    """

    def format(self, record):
        total_width = 50
        around_dash_place = 5

        logger_name = record.name

        # время: "HH:MM:SS" (8 символов) + ": " (2 символа) = 10 символов
        time_part_length = 10
        name_length = len(logger_name)

        dash_quantity = total_width - time_part_length - name_length - around_dash_place

        # Создаем разделитель динамической длины
        separator = ' ' * 3 + '-' * dash_quantity + ' ' * 2

        formatted_levelname = ' -' + ' ' + record.levelname + ' ' + '-' * (8 - len(record.levelname)) + '---- '

        formatted_message = f"{logger_name}{separator}{record.getMessage()}"

        result = f"{self.formatTime(record, self.datefmt)}{formatted_levelname}{formatted_message}"

        return result
