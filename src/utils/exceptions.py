class BadDCAOrderException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"BadDCAOrderException: {self.message}"

class NotYetImplemented(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"NotYetImplemented: {self.message}"

class UnimplementedAndNotPlanned(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"UnimplementedAndNotPlanned: {self.message}"