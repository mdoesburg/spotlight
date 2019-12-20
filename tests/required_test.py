from src.spotlight.errors import REQUIRED_ERROR
from .validator_test import ValidatorTest


class RequiredTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.required_error = REQUIRED_ERROR.format(field=self.field)
        self.rules = {"test": "required"}

    def test_required_rule_with_no_input_expect_error(self):
        data = {}
        expected = self.required_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_rule_with_string_expect_no_error(self):
        data = {"test": "this is a string"}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_rule_with_integer_one_expect_no_error(self):
        data = {"test": 1}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_rule_with_integer_zero_expect_no_error(self):
        data = {"test": 0}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_rule_with_boolean_false_expect_no_error(self):
        data = {"test": False}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_rule_with_boolean_true_expect_no_error(self):
        data = {"test": True}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_rule_with_empty_list_expect_error(self):
        data = {"test": []}
        expected = self.required_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_rule_with_list_expect_no_error(self):
        data = {"test": ["hello"]}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_required_rule_with_none_expect_error(self):
        data = {"test": None}
        expected = self.required_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_rule_with_empty_string_expect_error(self):
        data = {"test": ""}
        expected = self.required_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_rule_with_spaces_expect_error(self):
        data = {"test": "     "}
        expected = self.required_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_rule_with_empty_dict_expect_error(self):
        data = {"test": dict()}
        expected = self.required_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_required_rule_with_dict_expect_no_error(self):
        data = {"test": {"hello": "world"}}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)
