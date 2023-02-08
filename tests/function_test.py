from unittest.mock import MagicMock

from .validator_test import ValidatorTest


class FunctionTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_when_lambda_returns_error_expect_input_error(self):
        rules = {"test": [lambda value, validator, **kwargs: "error"]}
        data = {"test": "some_data"}
        expected = "error"

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_when_lambda_returns_none_expect_no_error(self):
        rules = {"test": [lambda value, validator, **kwargs: None]}
        data = {"test": "some_data"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_when_function_returns_error_expect_input_error(self):
        def validate(**_):
            return "error"

        rules = {"test": [validate]}
        data = {"test": "some_data"}
        expected = "error"

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_when_function_returns_none_expect_no_error(self):
        def validate(**_):
            return None

        rules = {"test": [validate]}
        data = {"test": "some_data"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_when_using_function_validator_expect_correct_arguments(self):
        mock = MagicMock(return_value=None)
        value = "some_data"
        rules = {"test": [mock]}
        data = {"test": value}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
        mock.assert_called_with(field=self.field, value=value, validator=self.validator)

    def test_function_with_implicit_flag_expect_error(self):
        def implicit_rule(value, **_):
            if not value:
                return "Required!"

        implicit_rule.implicit = True

        rules = {"test": [implicit_rule]}
        data = {}
        expected = ["Required!"]

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_function_with_multiple_non_stopping_implicit_rules_expect_errors(self):
        def implicit_rule(**_):
            return "Error!"

        implicit_rule.implicit = True

        rules = {"test": [implicit_rule, implicit_rule]}
        data = {}
        expected = ["Error!", "Error!"]

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_function_with_implicit_and_stop_flag_expect_error(self):
        def implicit_rule(**_):
            return "Error!"

        implicit_rule.implicit = True
        implicit_rule.stop = True

        rules = {"test": [implicit_rule, implicit_rule]}
        data = {}
        expected = ["Error!"]

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
