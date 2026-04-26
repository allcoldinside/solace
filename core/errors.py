"""Domain errors."""

class SolaceError(Exception):
    """Base SOLACE exception."""

class AuthError(SolaceError):
    """Authentication or authorization failure."""

class InvariantError(SolaceError):
    """Report or pipeline invariant failure."""
