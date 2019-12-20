from src.spotlight.errors import DICT_ERROR, REQUIRED_ERROR
from .validator_test import ValidatorTest


class DictTest(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.rules = {"test": "dict"}
        self.dict_error = DICT_ERROR.format(field=self.field)

    def test_dict_rule_with_set_expect_error(self):
        data = {"test": set()}
        expected = self.dict_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_dict_rule_with_dict_expect_no_error(self):
        data = {"test": {}}
        expected = None

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_dict_rule_and_required_with_empty_dict_expect_error(self):
        rules = {"test": "required|dict"}
        data = {"test": {}}
        expected = REQUIRED_ERROR.format(field=self.field)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_dict_rule_and_required_with_non_empty_dict_expect_no_error(self):
        rules = {"test": "required|dict"}
        data = {"test": {"field": "value"}}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_valid_dict_with_invalid_values_expect_false(self):
        invalid_dicts = ["0", "1", -1, 0, 1, 2, [], True, False, list(), set()]

        for invalid_dict in invalid_dicts:
            actual = self.validator.valid_dict(invalid_dict)
            self.assertEqual(actual, False)

    def test_valid_dict_with_valid_values_expect_true(self):
        valid_dicts = [{}, dict()]

        for valid_dict in valid_dicts:
            actual = self.validator.valid_dict(valid_dict)
            self.assertEqual(actual, True)
