class MatchingError(Exception):
    pass


class ValidationError(MatchingError):
    pass


class RiskError(MatchingError):
    pass


class UnknownOrder(MatchingError):
    pass
