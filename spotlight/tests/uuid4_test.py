from uuid import uuid4

from spotlight import errors as err
from spotlight.tests.validator_test import ValidatorTest


class Uuid4Test(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.uuid4_error = err.UUID4_ERROR.format(field=self.field)
        self.rules = {
            "test": "uuid4"
        }

    def test_uuid4_rule_with_invalid_string_expect_error(self):
        input_values = {
            "test": "1234"
        }
        expected = self.uuid4_error

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_uuid4_rule_with_integer_expect_error(self):
        input_values = {
            "test": 1234
        }
        expected = err.UUID4_ERROR.format(field=self.field)

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_uuid4_rule_with_boolean_true_expect_error(self):
        input_values = {
            "test": True
        }
        expected = err.UUID4_ERROR.format(field=self.field)

        errors = self.validator.validate(input_values, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_uuid4_rule_with_generated_uuid4_expect_no_error(self):
        rules = {
            "test": "uuid4"
        }
        input_values = {
            "test": uuid4()
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_uuid4_rule_with_string_expect_no_error(self):
        rules = {
            "test": "uuid4"
        }
        input_values = {
            "test": "a546ce64-634b-43b3-9c32-3f0353edb294"
        }
        expected = None

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_uuid4_rule_with_empty_string_expect_error(self):
        rules = {
            "test": "uuid4"
        }
        input_values = {
            "test": ""
        }
        expected = self.uuid4_error

        errors = self.validator.validate(input_values, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
