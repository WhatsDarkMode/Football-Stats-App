class FootballAppError(Exception):
    def __init__(self, message, status=None, code=None):
        self.message = message
        self.status = status
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f"Error message: {self.message}, Code: {self.code}, Status: {self.status}"

class UploadError(FootballAppError):
    def __init__(self, message, status="upload_err", code=None):
        super().__init__(message, status, code)


# class ErrorDataValidation(FootballAppError):
#     def __init__(self, message, code=None):
#         super().__init__(message, code=code or "Unknown")


# class ErrorDownload(FootballAppError):
#     def __init__(self, message, code=None):
#         super().__init__(message, code=code or "Unknown")


class DataProcessingError(FootballAppError):
    def __init__(self, message, function, code=None):
        super().__init__(message, code=code or "Unknown")


# class ErrorPlayerStatsTable(FootballAppError):
#     def __init__(self, message, code=None):
#         super().__init__(message, code=code or "Unknown")


class MissingFileError(FootballAppError):
    def __init__(self, message, code=None):
        super().__init__(message, code=code or "MissingFile")


class EmptyFileError(FootballAppError):
    def __init__(self, message, code=None):
        super().__init__(message, code=code or "EmptyFile")


class JsonLoadError(FootballAppError):
    def __init__(self, message, code=None):
        super().__init__(message, code=code or "JsonLoadError")