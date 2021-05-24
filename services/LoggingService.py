class LoggingService:

    def log_starting_progress(self, command, *suffix):
        if suffix:
            message = f'{command}:{suffix} '
        else:
            message = f'{command} '
        message += "in progress"
        self.log(message.capitalize())

    @staticmethod
    def log(message):
        print(message)
