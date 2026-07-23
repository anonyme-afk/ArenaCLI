class ArenaCLIError(Exception):
    """Base exception for ArenaCLI"""
    pass

class BrowserInitError(ArenaCLIError):
    """Raised when the browser fails to initialize"""
    pass

class LoginRequiredError(ArenaCLIError):
    """Raised when the user needs to login"""
    pass

class ElementNotFoundError(ArenaCLIError):
    """Raised when a UI element cannot be found"""
    pass

class GenerationTimeoutError(ArenaCLIError):
    """Raised when model generation times out"""
    pass
