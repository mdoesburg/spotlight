import unittest
from unittest import mock

from spotlight.validator import Validator


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
