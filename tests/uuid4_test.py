from uuid import uuid4, UUID

from src.spotlight.errors import UUID4_ERROR
from .validator_test import ValidatorTest


class Uuid4Test(ValidatorTest):
    def setUp(self):
        self.field = "test"
        self.uuid4_error = UUID4_ERROR.format(field=self.field)
        self.rules = {"test": "uuid4"}

    def test_uuid4_rule_with_invalid_string_expect_error(self):
        data = {"test": "1234"}
        expected = self.uuid4_error

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_uuid4_rule_with_integer_expect_error(self):
        data = {"test": 1234}
        expected = UUID4_ERROR.format(field=self.field)

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_uuid4_rule_with_boolean_true_expect_error(self):
        data = {"test": True}
        expected = UUID4_ERROR.format(field=self.field)

        errors = self.validator.validate(data, self.rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_uuid4_rule_with_generated_uuid4_expect_no_error(self):
        rules = {"test": "uuid4"}
        data = {"test": uuid4()}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_uuid4_rule_with_string_expect_no_error(self):
        rules = {"test": "uuid4"}
        data = {"test": "a546ce64-634b-43b3-9c32-3f0353edb294"}
        expected = None

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs, expected)

    def test_uuid4_rule_with_empty_string_expect_error(self):
        rules = {"test": "uuid4"}
        data = {"test": ""}
        expected = self.uuid4_error

        errors = self.validator.validate(data, rules)
        errs = errors.get(self.field)

        self.assertEqual(errs[0], expected)

    def test_valid_uuid4_with_invalid_values_expect_false(self):
        invalid_uuid4s = [True, False, -1, 0, 1, 2, [], {}, "", "123"]

        for invalid_uuid4 in invalid_uuid4s:
            actual = self.validator.valid_uuid4(invalid_uuid4)
            self.assertEqual(actual, False)

    def test_valid_uuid4_with_valid_values_expect_true(self):
        values = [
            "a546ce64-634b-43b3-9c32-3f0353edb294",
            uuid4(),
            UUID("{12345678-1234-5678-1234-567812345678}", version=4),
            UUID("12345678123456781234567812345678", version=4),
            UUID("urn:uuid:12345678-1234-5678-1234-567812345678", version=4),
            UUID(bytes=b"\x12\x34\x56\x78"*4, version=4),
            UUID(
                bytes_le=b"\x78\x56\x34\x12\x34\x12\x78\x56\x12\x34\x56\x78\x12\x34\x56\x78",
                version=4,
            ),
            UUID(
                fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678),
                version=4,
            ),
            UUID(int=0x12345678123456781234567812345678, version=4),
        ]

        for value in values:
            actual = self.validator.valid_uuid4(value)
            self.assertEqual(actual, True)
