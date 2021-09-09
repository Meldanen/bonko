class LoggingService:

    def log_starting_process(self, command, *suffix):
        if suffix:
            message = f'{command}:{suffix} '
        else:
            message = f'{command} '
        message += "in progress"
        self.log(message.capitalize())

    @staticmethod
    def log(message):
        print(message)

    @staticmethod
    def exception(message):
        print(message)
