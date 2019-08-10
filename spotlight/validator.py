import re
from string import Formatter
from typing import Union, List, overload, Generator, Tuple, Iterator, Dict

from spotlight import rules as rls
from spotlight.exceptions import RuleNotFoundError, InvalidInputError, InvalidRulesError


class Validator:
    """
    Creates an instance of the Validator class.

    Parameters
    ----------
    plugins : list
        A list of plugins that add additional validation rules.
    """

    class Plugin:
        """
        Creates an instance of the Validator Plugin class.
        """

        def rules(self) -> List[rls.Rule]:
            return []

    def __init__(self, plugins: List[Plugin] = None):
        self._data = None
        self._rules = None
        self._output = {}
        self._flat_list = []
        self._current_field = None
        self._current_rule = None

        self.overwrite_messages = {}
        self.overwrite_fields = {}
        self.overwrite_values = {}

        self._implicit_rules: List[str] = []
        self._available_rules: Dict[str, rls.Rule] = {}
        self._stopped_fields = []

        self.FIELD_WILD_CARD = "*"
        self._FIELD_DELIMITER = "."
        self._RULE_DELIMITER = "|"
        self._RULE_VALUE_DELIMITER = ":"

        self.validation_order = {}

        self._setup_default_rules()
        self._setup_plugins(plugins or [])

    def _setup_default_rules(self):
        self.register_rules(self._default_rules())

    def register_rules(self, rules: [rls.Rule]):
        for rule in rules:
            self.register_rule(rule)

    def register_rule(self, rule: rls.Rule):
        self._setup_rule(rule)

    def _setup_rule(self, rule):
        self._available_rules[rule.name] = rule
        if rule.implicit:
            self._implicit_rules.append(rule.name)

    @staticmethod
    def _default_rules() -> List[rls.Rule]:
        return [rule() for rule in rls.Rule.subclasses]

    def _setup_plugins(self, plugins: List[Plugin]):
        for plugin in plugins:
            self.register_rules(plugin.rules())

    @staticmethod
    def _dynamically_add_static_validation_methods(rule):
        for attr in dir(rule):
            if attr.startswith("valid_"):
                validation_method = getattr(rule, attr)
                setattr(Validator, attr, staticmethod(validation_method))

    @overload
    def validate(
        self, data: dict, rules: dict, flat: bool = False
    ) -> Union[dict, list]:
        ...

    @overload
    def validate(
        self, data: object, rules: dict, flat: bool = False
    ) -> Union[dict, list]:
        ...

    def validate(
        self, data: Union[dict, object], rules: dict, flat: bool = False
    ) -> Union[dict, list]:
        """
        Validate data with given rules.

        Parameters
        ----------
        data : dict or object
            Dict or object that can be converted to a dict with data that needs
            to be validated.
            For example: {"email": "john.doe@example.com"},
            CustomDataClass(email="john.doe@example.com")
        rules : dict
            Dict with validation rules for the given data.
            For example: {"email": "required|email|unique:user,email"}
        flat : bool, optional
            Returns a list of errors instead of a dict if true.

        Returns
        -------
        errors : dict or list
            Dict or list of errors. When a dict of errors is returned, each key
            represents the field name, and the corresponding value is a list of
            errors for that key/field. When the optional parameter `flat` is
            set to true, a list of only the error messages is returned.
        """
        self._data = data
        self._rules = rules
        self._output = {}
        self._stopped_fields = []

        self._validate_data()

        if flat:
            self._flat_list = []
            self._flatten_output(self._output)

            return self._flat_list

        return self._output

    def _test(self, field):
        if not self._contains_wildcard(field):
            yield field
            return

        root = field.split(self.FIELD_WILD_CARD)[0].strip(self._FIELD_DELIMITER)
        root_value = self._get_field_value(root)

        if isinstance(root_value, list):
            for i, _ in enumerate(root_value):
                new_field = field.replace(self.FIELD_WILD_CARD, str(i), 1)
                yield from self._test(new_field)

    def _validate_data(self):
        self._convert_data_to_dict()
        self._validate_rules_type()

        # Iterate over fields
        for field, rules in self._field_iterator():
            # for field in self._test(f):
            #     # print(f)

            # Iterate over rules
            for rule, rule_name in rules:
                # Check if rule exists
                if not self._rule_exists(rule_name):
                    raise RuleNotFoundError(rule_name)

                # Check if field is validatable
                if self._is_validatable(rule_name, field):
                    self._validate_field(field, rule)

                    # Stop
                    if self._current_field in self._stopped_fields:
                        # print(f"---- stop ({self._current_field}) ----")
                        break

        # for key, val in self.validation_order.items():
        #     print(key, "|", val)

    def _field_iterator(self) -> Iterator[Tuple[str, Iterator[Tuple[str, str]]]]:
        for field, rules in self._rules.items():
            yield field, self._rule_iterator(self._split_rules(rules))

    def _rule_iterator(self, rules) -> Iterator[Tuple[str, str]]:
        for rule in rules:
            yield rule, self._rule_name(rule)

    def _split_rules(self, rules: str) -> list:
        return rules.split(self._RULE_DELIMITER)

    def _rule_name(self, rule: str) -> str:
        return self._split_rule(rule)[0]

    def _rule_values(self, rule: str) -> str:
        if self._RULE_VALUE_DELIMITER in rule:
            return self._split_rule(rule)[1]

    def _split_rule(self, rule: str) -> List[str]:
        return rule.split(self._RULE_VALUE_DELIMITER)

    def _convert_data_to_dict(self):
        if not isinstance(self._data, dict):
            try:
                self._data = self._data.__dict__
            except AttributeError:
                raise InvalidInputError(type(self._data))

    def _validate_rules_type(self):
        if type(self._rules) is not dict:
            raise InvalidRulesError(type(self._rules))

    def _rule_exists(self, rule_name: str) -> bool:
        return rule_name in self._available_rules

    def _iterate_wildcards(self, field, rule):
        root = field.split(self.FIELD_WILD_CARD)[0].strip(self._FIELD_DELIMITER)
        if root in self._stopped_fields:
            return

        root_value = self._get_field_value(root)
        if type(root_value) is list:
            for index, val in enumerate(root_value):
                new_field = field.replace(self.FIELD_WILD_CARD, str(index), 1)
                self._validate_field(new_field, rule)
        else:
            new_field = field.replace(self.FIELD_WILD_CARD, "0", 1)
            self._validate_field(new_field, rule)

    def _validate_field_new(self, field, rule):
        self._current_field = field
        self._current_rule = rule

        if field in self._stopped_fields:
            return

        self.validation_order[field] = rule

        value = self._get_field_value(field)
        rule_name = self._rule_name(rule)
        rule_values = self._rule_values(rule)
        matched_rule = self._available_rules.get(rule_name)

        # If rule didn't pass, add error
        if not matched_rule.passes(field, value, rule_values, self._data):
            self._add_error(matched_rule)

            if matched_rule.stop:
                self._stopped_fields.append(field)

    def _validate_field(self, field, rule):
        self._current_field = field
        self._current_rule = rule

        if field in self._stopped_fields:
            return

        if self._contains_wildcard(field):
            self._iterate_wildcards(field, rule)
            return

        self.validation_order[field] = rule

        value = self._get_field_value(field)
        rule_name = self._rule_name(rule)
        rule_values = self._rule_values(rule)
        matched_rule = self._available_rules.get(rule_name)

        # If rule didn't pass, add error
        if not matched_rule.passes(field, value, rule_values, self._data):
            self._add_error(matched_rule)

            if matched_rule.stop:
                self._stopped_fields.append(field)

    def _contains_wildcard(self, value):
        return self.FIELD_WILD_CARD in value

    def _is_validatable(self, rule: str, field: str) -> bool:
        return self._present_or_rule_is_implicit(rule, field)

    def _present_or_rule_is_implicit(self, rule: str, field: str) -> bool:
        return self._validate_present(field) or self._is_implicit(rule)

    def _validate_present(self, field: str) -> bool:
        field = field.replace(self.FIELD_WILD_CARD, "0")

        return self._get_field_value(field) is not None

    def _is_implicit(self, rule: str) -> bool:
        return rule in self._implicit_rules

    def _add_error(self, matched_rule):
        field = matched_rule.message_fields.get("field")
        error = self._create_error(matched_rule)

        if field in self._output:
            self._output.get(field).append(error)
        else:
            self._output[field] = [error]

    def _create_error(self, matched_rule):
        rule = matched_rule.name
        error = matched_rule.message
        fields = matched_rule.message_fields
        field = fields.get("field")

        # result = [x[1] for x in Formatter().parse(error) if x[1] is not None]
        # result = re.findall("{(.*?)}", error)
        # print(result)

        # print(rule, field, error, fields, sep=" | ")

        wildcard_field = self._convert_field_to_wildcard_field(field)
        combined_field = wildcard_field + self._FIELD_DELIMITER + rule
        # print(wildcard_field, "|", combined_field)
        if wildcard_field in self.overwrite_messages:
            error = self.overwrite_messages[wildcard_field]
        if combined_field in self.overwrite_messages:
            error = self.overwrite_messages[combined_field]

        fields = self._overwrite_fields(fields)

        if wildcard_field in self.overwrite_values:
            fields["values"] = self.overwrite_values[wildcard_field]["values"]

        return error.format(**fields)

    def _overwrite_fields(self, fields):
        for overwrite_field, overwrite_value in self.overwrite_fields.items():
            for key, value in fields.items():
                value = self._convert_field_to_wildcard_field(value)
                if overwrite_field == value:
                    fields[key] = overwrite_value

        return fields

    def _convert_field_to_wildcard_field(self, field) -> str:
        split_fields = str(field).split(self._FIELD_DELIMITER)
        for index, field in enumerate(split_fields):
            if field.isnumeric():
                split_fields[index] = self.FIELD_WILD_CARD

        return self._FIELD_DELIMITER.join(split_fields)

    def _flatten_output(self, output: dict):
        for field, errors in output.items():
            if type(errors) is dict:
                self._flatten_output(errors)
                continue
            for error in errors:
                self._flat_list.append(error)

    def _get_field_value(self, field):
        value = self._data
        split_field = field.split(self._FIELD_DELIMITER)

        try:
            for key in split_field:
                if not isinstance(value, dict) and not isinstance(value, list):
                    value = value.__dict__
                if key.isnumeric():
                    value = value[int(key)]
                else:
                    value = value.get(key)
        except (TypeError, AttributeError, KeyError, IndexError):
            return None

        return value

    @staticmethod
    def valid_email(email) -> bool:
        return rls.EmailRule.valid_email(email)

    @staticmethod
    def valid_url(url) -> bool:
        return rls.UrlRule.valid_url(url)

    @staticmethod
    def valid_ip(ip) -> bool:
        return rls.IpRule.valid_ip(ip)

    @staticmethod
    def valid_uuid4(uuid) -> bool:
        return rls.Uuid4Rule.valid_uuid4(uuid)

    @staticmethod
    def valid_string(string) -> bool:
        return rls.StringRule.valid_string(string)

    @staticmethod
    def valid_integer(integer) -> bool:
        return rls.IntegerRule.valid_integer(integer)

    @staticmethod
    def valid_float(float_) -> bool:
        return rls.FloatRule.valid_float(float_)

    @staticmethod
    def valid_boolean(boolean) -> bool:
        return rls.BooleanRule.valid_boolean(boolean)

    @staticmethod
    def valid_json(value) -> bool:
        return rls.JsonRule.valid_json(value)

    @staticmethod
    def valid_alpha_num(value) -> bool:
        return rls.AlphaNumRule.valid_alpha_num(value)

    @staticmethod
    def valid_alpha_num_space(value) -> bool:
        return rls.AlphaNumSpaceRule.valid_alpha_num_space(value)

    @staticmethod
    def valid_list(value) -> bool:
        return rls.ListRule.valid_list(value)

    @staticmethod
    def valid_dict(value) -> bool:
        return rls.DictRule.valid_dict(value)

