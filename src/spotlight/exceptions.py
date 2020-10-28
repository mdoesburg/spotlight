class RuleNotFoundError(Exception):
    def __init__(self, rule: str):
        super().__init__(f"the '{rule}' rule does not exist")


class RuleNameAlreadyExistsError(Exception):
    def __init__(self, rule: str):
        super().__init__(f"the rule name '{rule}' already exists")


class InvalidDataError(Exception):
    def __init__(self, data_type: type):
        super().__init__(
            f"expected 'dict' or an 'object' that can be converted to a 'dict' got '{data_type}'"
        )


class InvalidRulesError(Exception):
    def __init__(self, rules_type: type):
        super().__init__(f"expected 'dict' got '{rules_type}'")


class AttributeNotImplementedError(Exception):
    def __init__(self, attribute: str, class_name: str):
        super().__init__(
            f"the class '{class_name}' is missing the '{attribute}' attribute"
        )


class FieldValueNotFoundError(Exception):
    pass


class InvalidDateTimeFormat(Exception):
    def __init__(self):
        super().__init__("invalid date time format")
