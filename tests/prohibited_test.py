from src.spotlight.errors import PROHIBITED_ERROR
from .validator_test import ValidatorTest


class ProhibitedTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.error = PROHIBITED_ERROR.format(field=self.field)
        self.rules = {"test": "prohibited"}

    def test_prohibited_rule_with_no_input_expect_no_error(self):
        data = {}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertFalse(errs, expected)

    def test_prohibited_rule_with_string_expect_error(self):
        data = {"test": "this is a string"}
        expected = self.error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_rule_with_integer_one_expect_error(self):
        data = {"test": 1}
        expected = self.error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_rule_with_integer_zero_expect_error(self):
        data = {"test": 0}
        expected = self.error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_rule_with_boolean_false_expect_error(self):
        data = {"test": False}
        expected = self.error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_rule_with_boolean_true_expect_error(self):
        data = {"test": True}
        expected = self.error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_rule_with_empty_list_expect_no_error(self):
        data = {"test": []}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_rule_with_list_expect_error(self):
        data = {"test": ["hello"]}
        expected = self.error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_prohibited_rule_with_none_expect_no_error(self):
        data = {"test": None}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_rule_with_empty_string_expect_no_error(self):
        data = {"test": ""}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_rule_with_spaces_expect_no_error(self):
        data = {"test": "     "}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_rule_with_empty_dict_expect_no_error(self):
        data = {"test": dict()}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_prohibited_rule_with_dict_expect_error(self):
        data = {"test": {"hello": "world"}}
        expected = self.error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)
