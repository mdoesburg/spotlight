from .validator_test import ValidatorTest


class FunctionTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_when_lambda_returns_error_expect_input_error(self):
        rules = {"test": [lambda value, validator: "error"]}
        data = {"test": "some_data"}
        expected = "error"

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_when_lambda_returns_none_expect_input_error(self):
        rules = {"test": [lambda value, validator: None]}
        data = {"test": "some_data"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_when_function_returns_error_expect_input_error(self):
        def validate(*_, **__):
            return "error"

        rules = {"test": [validate]}
        data = {"test": "some_data"}
        expected = "error"

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_when_function_returns_none_expect_input_error(self):
        def validate(*_, **__):
            return None

        rules = {"test": [validate]}
        data = {"test": "some_data"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
