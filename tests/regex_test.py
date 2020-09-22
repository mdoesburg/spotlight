from src.spotlight.errors import REGEX_ERROR
from .validator_test import ValidatorTest


class RegexTest(ValidatorTest):
    def setUp(self):
        self.field = "test"

    def test_regex_rule_with_email_regex_with_invalid_value_expect_error(self):
        regex = "^.+@.+$"
        rules = {"test": f"regex:{regex}"}
        data = {"test": "this.is.not.a.valid.email"}
        expected = REGEX_ERROR.format(field=self.field, regex=regex)

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_regex_rule_with_email_regex_with_valid_value_expect_no_error(self):
        regex = "^.+@.+$"
        rules = {"test": f"regex:{regex}"}
        data = {"test": "john.doe@example.com"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_regex_rule_with_date_time_regex_with_valid_value_expect_no_error(self):
        regex = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        rules = {"test": f"regex:{regex}"}
        data = {"test": "2020-01-20 12:00:00"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_regex_rule_with_regex_containing_pipe_with_valid_value_expect_no_error(
        self
    ):
        regex = "a|b"
        rules = {"test": ["string", f"regex:{regex}"]}
        data = {"test": "a"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_regex_rule_with_valid_values_expect_no_errors(self):
        rules = {
            "test1": "regex:abc*",
            "test2": "regex:abc{2}",
            "test3": "regex:a[bc]",
            "test4": r"regex:\D",
            "test5": r"regex:^\S+@\S+$",
        }
        data = {
            "test1": "abccc",
            "test2": "abcc",
            "test3": "ac",
            "test4": "a",
            "test5": "test@example.com",
        }
        expected = 0

        errors = self.validator.validate(data, rules)

        self.assertEqual(len(errors), expected)

    def test_regex_rule_with_invalid_values_expect_errors(self):
        regex = ["abc*", "abc{2}", "a[bc]", r"\D", r"^\S+@\S+$"]
        rules = {
            "test1": f"regex:{regex[0]}",
            "test2": f"regex:{regex[1]}",
            "test3": f"regex:{regex[2]}",
            "test4": f"regex:{regex[3]}",
            "test5": f"regex:{regex[4]}",
        }
        data = {
            "test1": "abd",
            "test2": "abccc",
            "test3": "ad",
            "test4": "1",
            "test5": "invalid.email",
        }

        errors = self.validator.validate(data, rules)

        for i, (field, err) in enumerate(errors.items()):
            expected = REGEX_ERROR.format(field=field, regex=regex[i])
            self.assertEqual(err[0], expected)
