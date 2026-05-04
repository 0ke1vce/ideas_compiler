class ErrorHandler:
    def __init__(self):
        self.has_error = False

    def report_error(self, phase, line_number, message):
        self.has_error = True
        red_text = "\033[91m"
        reset_text = "\033[0m"
        print(f"{red_text}[{phase} Error] Line {line_number}: {message}{reset_text}")

    def report_warning(self, phase, line_number, message):
        yellow_text = "\033[93m"
        reset_text = "\033[0m"
        print(f"{yellow_text}[{phase} Warning] Line {line_number}: {message}{reset_text}")