class DelabaError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RootEntityViolationError(DelabaError):
    pass


class LLMGenerationError(DelabaError):
    pass
