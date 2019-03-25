from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class BooleanTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.boolean_error = err.BOOLEAN_ERROR.format(field=self.field)

    def test_boolean_rule_with_string_expect_error(self):
        rules = {
            "test": "boolean"
        }
        input_values = {
            "test": "test"
        }
        expected = self.boolean_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_boolean_rule_with_integer_one_expect_error(self):
        rules = {
            "test": "boolean"
        }
        input_values = {
            "test": 1
        }
        expected = self.boolean_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_boolean_rule_with_boolean_false_expect_no_error(self):
        rules = {
            "test": "boolean"
        }
        input_values = {
            "test": False
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_boolean_rule_with_boolean_true_expect_no_error(self):
        rules = {
            "test": "boolean"
        }
        input_values = {
            "test": True
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_boolean_with_string_expect_false(self):
        valid_boolean = self.validator.valid_boolean("invalid.boolean")

        self.assertEqual(valid_boolean, False)

    def test_valid_boolean_with_integer_ten_expect_false(self):
        valid_boolean = self.validator.valid_boolean(10)

        self.assertEqual(valid_boolean, False)

    def test_valid_boolean_with_boolean_true_expect_true(self):
        valid_boolean = self.validator.valid_boolean(True)

        self.assertEqual(valid_boolean, True)

    def test_valid_boolean_with_boolean_false_expect_true(self):
        valid_boolean = self.validator.valid_boolean(False)

        self.assertEqual(valid_boolean, True)
