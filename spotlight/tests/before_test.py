from spotlight.tests.validator_test import ValidatorTest


class BeforeTest(ValidatorTest):
    def test_before_rule_with_valid_values(self):
        rules = {
            "start_time": "date_time|before:end_time",
            "end_time": "date_time",
        }
        data = {
            "start_time": "2019-08-24 16:28:00",
            "end_time": "2019-08-24 16:48:00",
        }
        expected = {}

        errors = self.validator.validate(data, rules)

        self.assertEqual(errors, expected)
