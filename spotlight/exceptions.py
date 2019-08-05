class RuleNotFoundError(Exception):
    def __init__(self, rule):
        super().__init__(f"The '{rule}' rule does not exist")
