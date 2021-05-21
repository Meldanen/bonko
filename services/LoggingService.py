

class LoggingService:


    def log_starting_progress(self, command):
        self.log(f'{command} in progress')

    @staticmethod
    def log(message):
        print(message)