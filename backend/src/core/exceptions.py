class AppError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RootEntityViolationError(AppError):
    pass


class LLMGenerationError(AppError):
    pass
