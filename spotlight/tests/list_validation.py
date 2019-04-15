from spotlight.tests.validator_test import ValidatorTest


class ListValidationTest(ValidatorTest):
    def setUp(self):
        self.validator.overwrite_messages = {}
        self.validator.overwrite_fields = {}
        self.validator.overwrite_values = {}

    def test_list_validation_expect_error(self):
        rules = {"list": {"test": "max:2", "test2": "min:2"}}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list": {
                "test": [
                    "The test field cannot be longer than 2 characters.",
                    "The test field cannot be longer than 2 characters.",
                ],
                "test2": [
                    "The test2 field has to be at least 2 characters.",
                    "The test2 field has to be at least 2 characters.",
                    "The test2 field has to be at least 2 characters.",
                ],
            }
        }

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_list_validation_flat_expect_error(self):
        rules = {"list": {"test": "max:2", "test2": "min:2"}}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = [
            "The test field cannot be longer than 2 characters.",
            "The test field cannot be longer than 2 characters.",
            "The test2 field has to be at least 2 characters.",
            "The test2 field has to be at least 2 characters.",
            "The test2 field has to be at least 2 characters.",
        ]

        errors = self.validator.validate(input_values, rules, flat=True)
        self.assertEqual(expected, errors)

    def test_list_validation_expect_with_custom_message_error(self):
        rules = {"list": {"test": "max:2", "test2": "min:2"}}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list": {
                "test": [
                    "Hey! The test field has to be at least 2 chars!",
                    "Hey! The test field has to be at least 2 chars!",
                ],
                "test2": [
                    "The test2 field has to be at least 2 characters.",
                    "The test2 field has to be at least 2 characters.",
                    "The test2 field has to be at least 2 characters.",
                ],
            }
        }

        new_message = "Hey! The {field} field has to be at least {max} chars!"
        messages = {"test.max": new_message}
        self.validator.overwrite_messages = messages

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_list_validation_expect_with_custom_fields_error(self):
        rules = {"list": {"test": "max:2", "test2": "min:2"}}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list": {
                "test": [
                    "The test field cannot be longer than 2 characters.",
                    "The test field cannot be longer than 2 characters.",
                ],
                "test2": [
                    "The custom field has to be at least 2 characters.",
                    "The custom field has to be at least 2 characters.",
                    "The custom field has to be at least 2 characters.",
                ],
            }
        }

        fields = {"test2": "custom"}
        self.validator.overwrite_fields = fields

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_list_validation_expect_with_values_message_error(self):
        rules = {"list": {"test": "max:2", "test2": "in:val1,val2,val3"}}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test": "123", "test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list": {
                "test": [
                    "The test field cannot be longer than 2 characters.",
                    "The test field cannot be longer than 2 characters.",
                ],
                "test2": [
                    "The test2 field must be one of the following values: "
                    "piet, henk, jan.",
                    "The test2 field must be one of the following values: "
                    "piet, henk, jan.",
                    "The test2 field must be one of the following values: "
                    "piet, henk, jan.",
                ],
            }
        }

        new_values = "piet, henk, jan"
        values = {"test2": {"values": new_values}}
        self.validator.overwrite_values = values

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_list_validation_required_expect_error(self):
        rules = {"list": {"test": "required|max:2", "test2": "min:2"}}
        input_values = {
            "list": [
                {"test": "12", "test2": "1"},
                {"test2": "1"},
                {"test": "1234", "test2": "1"},
            ]
        }
        expected = {
            "list": {
                "test": [
                    "The test field is required.",
                    "The test field cannot be longer than 2 characters.",
                ],
                "test2": [
                    "The test2 field has to be at least 2 characters.",
                    "The test2 field has to be at least 2 characters.",
                    "The test2 field has to be at least 2 characters.",
                ],
            }
        }

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_list_validation_with_optional_field_expect_no_error(self):
        rules = {"list": {"test": "max:2", "test2": "min:2"}}
        input_values = {"list": [{}, {}, {}]}
        expected = {}

        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)

    def test_list_validation_with_filled_field_expect_error(self):
        rules = {"list": {"test": "required|max:2", "test2": "min:2"}}
        input_values = {"list": [{}, {}, {}]}
        expected = {
            "list": {
                "test": [
                    "The test field is required.",
                    "The test field is required.",
                    "The test field is required.",
                ]
            }
        }
        errors = self.validator.validate(input_values, rules)
        self.assertEqual(expected, errors)
