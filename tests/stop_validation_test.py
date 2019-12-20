from src.spotlight import errors as err
from .validator_test import ValidatorTest


class StopValidationTest(ValidatorTest):
    def test_field_validation_will_stop_if_required(self):
        data = {"test1": "", "test2": "not.a.valid.email"}
        rules = {"test1": "required|email|min:1|max:255", "test2": "required|email"}

        errors = self.validator.validate(data, rules)
        err1 = errors.get("test1")
        err2 = errors.get("test2")

        self.assertEqual(len(errors), 2)
        self.assertEqual(len(err1), 1)
        self.assertEqual(len(err2), 1)
        self.assertEqual(err1[0], err.REQUIRED_ERROR.format(field="test1"))
        self.assertEqual(err2[0], err.EMAIL_ERROR.format(field="test2"))

    def test_nested_list_field_validation_will_stop_if_required(self):
        data = {"test": [{"test1": ""}, {"test1": "not.a.valid.email"}]}
        rules = {"test.*.test1": "required|email|min:1|max:255"}

        errors = self.validator.validate(data, rules)
        err1 = errors.get("test.0.test1")
        err2 = errors.get("test.1.test1")

        self.assertEqual(len(errors), 2)
        self.assertEqual(len(err1), 1)
        self.assertEqual(len(err2), 1)
        self.assertEqual(err1[0], err.REQUIRED_ERROR.format(field="test.0.test1"))
        self.assertEqual(err2[0], err.EMAIL_ERROR.format(field="test.1.test1"))

    def test_nested_dict_field_validation_will_stop_if_required(self):
        data = {"test": {"test1": "", "test2": "not.a.valid.email"}}
        rules = {
            "test.test1": "required|email|min:1|max:255",
            "test.test2": "required|email",
        }

        errors = self.validator.validate(data, rules)
        err1 = errors.get("test.test1")
        err2 = errors.get("test.test2")

        self.assertEqual(len(errors), 2)
        self.assertEqual(len(err1), 1)
        self.assertEqual(len(err2), 1)
        self.assertEqual(err1[0], err.REQUIRED_ERROR.format(field="test.test1"))
        self.assertEqual(err2[0], err.EMAIL_ERROR.format(field="test.test2"))
