import unittest
from unittest import mock

from src.spotlight.validator import Validator


class ValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = Validator()


class ValidatorPluginTest(unittest.TestCase):
    def test_plugin_rules_registered(self):
        plugin = Validator.Plugin()
        with mock.patch.object(plugin, "rules", wraps=plugin.rules) as m:
            Validator([plugin])
        m.assert_called()


class DirectValidationMethodsTest(ValidatorTest):
    def test_direct_validation_methods_are_present(self):
        methods = [attr for attr in dir(Validator) if attr.startswith("valid_")]

        self.assertEqual(len(methods) > 0, True)
        for name, rule in self.validator._available_rules.items():
            for attr in dir(rule):
                if attr.startswith("valid_"):
                    self.assertEqual(attr in methods, True)
