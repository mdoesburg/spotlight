from src.spotlight.errors import INTEGER_ERROR
from .validator_test import ValidatorTest


class IntegerTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.integer_error = INTEGER_ERROR.format(field=self.field)

    def test_integer_rule_with_string_expect_error(self):
        rules = {"test": "integer"}
        data = {"test": "test"}
        expected = self.integer_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_integer_rule_with_ten_expect_no_error(self):
        rules = {"test": "integer"}
        data = {"test": 10}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_integers_with_invalid_values_expect_false(self):
        invalid_integers = ["0", "1", -1.0, 1.4, [], {}, "test"]

        for invalid_integer in invalid_integers:
            actual = self.validator.valid_integer(invalid_integer)
            self.assertEqual(actual, False)

    def test_valid_integers_with_valid_values_expect_true(self):
        valid_integers = [-1, 0, 1, 5, 10, True, False]

        for valid_integer in valid_integers:
            actual = self.validator.valid_integer(valid_integer)
            self.assertEqual(actual, True)
