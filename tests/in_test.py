from src.spotlight.errors import IN_ERROR
from .validator_test import ValidatorTest


class InTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.in_error = IN_ERROR.format(field=self.field, values="val0, val1, val2")

    def test_in_rule_with_invalid_value_expect_error(self):
        data = {"test": "val3"}
        rules = {"test": "in:val0,val1,val2"}
        expected = self.in_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_in_rule_with_valid_value_expect_no_error(self):
        data = {"test": "val1"}
        rules = {"test": "in:val0,val1,val2"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_in_rule_with_various_string_capitalization_expect_no_error(self):
        data = {
            "case1": "camelCase",
            "case2": "snake_case",
            "case3": "kebab-case",
            "case4": "PascalCase",
            "case5": "lowercase",
            "case6": "UPPERCASE",
            "case7": "AlTcAsE",
        }
        valid_values = (
            "camelCase,snake_case,kebab-case,PascalCase,lowercase,UPPERCASE,AlTcAsE"
        )
        rules = {
            "case1": f"in:{valid_values}",
            "case2": f"in:{valid_values}",
            "case3": f"in:{valid_values}",
            "case4": f"in:{valid_values}",
            "case5": f"in:{valid_values}",
            "case6": f"in:{valid_values}",
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors.items()), 0)

    def test_in_rule_with_mismatching_capitalization_expect_error(self):
        data = {"test1": "VAL1", "test2": "vAl1", "test3": "VaL1"}
        rules = {
            "test1": "in:val0,val1,val2",
            "test2": "in:val0,VaL1,val2",
            "test3": "in:val0,vAl1,val2",
        }

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors), 3)

    def test_in_rule_with_integer_expect_no_error(self):
        data = {"test": 1}
        rules = {"test": "in:1,2,3"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_in_rule_with_bool_expect_no_error(self):
        data = {"test": True}
        rules = {"test": "in:True,False"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
