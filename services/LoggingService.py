class LoggingService:

    def log_starting_progress(self, command):
        message = f'{command} in progress'
        self.log(message.capitalize())

    @staticmethod
    def log(message):
        print(message)
