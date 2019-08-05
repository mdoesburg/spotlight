class RuleNotFoundError(Exception):
    def __init__(self, rule: str):
        super().__init__(f"the '{rule}' rule does not exist")


class InvalidInputError(Exception):
    def __init__(self, input_type: type):
        super().__init__(
            f"expected 'dict' or an 'object' that can be converted to a 'dict' got '{input_type}'"
        )


class InvalidRulesError(Exception):
    def __init__(self, rules_type: type):
        super().__init__(
            f"expected 'dict' got '{rules_type}'"
        )
