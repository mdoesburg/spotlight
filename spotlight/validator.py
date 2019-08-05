from typing import Union, List

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

        def rules(self) -> List[rls.BaseRule]:
            return []

    def __init__(self, plugins: List[Plugin] = None):
        self._input = None
        self._input_rules = None
        self._output = {}
        self._flat_list = []

        self.overwrite_messages = {}
        self.overwrite_fields = {}
        self.overwrite_values = {}

        self._implicit_rules = []
        self._registered_rules = []
        self._available_rules = {}
        self._stopped_fields = []

        self.FIELD_WILD_CARD = "*"

        self._setup_default_rules()
        self._setup_plugins(plugins or [])

    def _setup_default_rules(self):
        self.register_rules(self._default_rules())

    @staticmethod
    def _default_rules() -> List[rls.BaseRule]:
        return [
            rls.RequiredRule(),
            rls.RequiredWithoutRule(),
            rls.RequiredWithRule(),
            rls.RequiredIfRule(),
            rls.NotWithRule(),
            rls.FilledRule(),
            rls.EmailRule(),
            rls.UrlRule(),
            rls.IpRule(),
            rls.MinRule(),
            rls.MaxRule(),
            rls.InRule(),
            rls.AlphaNumRule(),
            rls.AlphaNumSpaceRule(),
            rls.StringRule(),
            rls.IntegerRule(),
            rls.FloatRule(),
            rls.BooleanRule(),
            rls.JsonRule(),
            rls.ListRule(),
            rls.Uuid4Rule(),
            rls.AcceptedRule(),
            rls.StartsWithRule(),
            rls.DictRule(),
        ]

    def _setup_rule(self, rule):
        self._available_rules[rule.name] = rule
        if rule.implicit:
            self._implicit_rules.append(rule.name)

    @staticmethod
    def _dynamically_add_static_validation_methods(rule):
        for attr in dir(rule):
            if attr.startswith("valid_"):
                validation_method = getattr(rule, attr)
                setattr(Validator, attr, staticmethod(validation_method))

    def register_rules(self, rules: [rls.BaseRule]):
        for rule in rules:
            self.register_rule(rule)

    def register_rule(self, rule: rls.BaseRule):
        self._registered_rules.append(rule)
        self._setup_rule(rule)

    def validate(
        self, input_: Union[dict, object], input_rules: dict, flat: bool = False
    ) -> Union[dict, list]:
        """
        Validate input with given rules.

        Parameters
        ----------
        input_ : dict or object
            Dict or object with input that needs to be validated.
            For example: {"email": "john.doe@example.com"},
            CustomInputClass(email="john.doe@example.com")
        input_rules : dict
            Dict with validation rules for given input.
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
        self._input = input_
        self._input_rules = input_rules
        self._output = {}
        self._stopped_fields = []

        self._validate_input()

        if flat:
            self._flat_list = []
            self._flatten_output(self._output)

            return self._flat_list

        return self._output

    def _validate_input(self):
        self._convert_input_to_dict()
        self._validate_input_rules()

        # Iterate over fields
        for field, field_rules in self._input_rules.items():
            rules = self._split_rules(field_rules)

            # Iterate over rules
            for rule in rules:
                rule_name = self._rule_name(rule)

                # Check if rule exists
                if not self._rule_exists(rule_name):
                    raise RuleNotFoundError(rule_name)

                # Check if field is validatable
                if self._is_validatable(rule_name, field):
                    self._validate_field(field, rule)

    def _split_rules(self, rules) -> list:
        return rules.split("|")

    def _rule_name(self, rule: str) -> str:
        return rule.split(":")[0]

    def _rule_values(self, rule) -> list:
        _, *rule_values = rule.split(":")
        return rule_values

    def _convert_input_to_dict(self):
        if not isinstance(self._input, dict):
            try:
                self._input = self._input.__dict__
            except AttributeError:
                raise InvalidInputError(type(self._input))

    def _validate_input_rules(self):
        if type(self._input_rules) is not dict:
            raise InvalidRulesError(type(self._input_rules))

    def _rule_exists(self, rule_name: str) -> bool:
        return rule_name in self._available_rules

    def _validate_field(self, field, rule):
        if field in self._stopped_fields:
            return

        if self._contains_wildcard(field):
            root = field.split(self.FIELD_WILD_CARD)[0].strip(".")
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

            return

        # Setup variables
        passed = False
        value = self._get_field_value(field)
        rule_name = self._rule_name(rule)
        rule_values = self._rule_values(rule)
        matched_rule = self._available_rules.get(rule_name)

        # Execute correct validation method: Rule vs Dependent Rule
        if isinstance(matched_rule, rls.Rule):
            passed = matched_rule.passes(field, value)
        elif isinstance(matched_rule, rls.DependentRule):
            passed = matched_rule.passes(field, value, rule_values, self._input)

        # If rule didn't pass, add error
        if not passed:
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
        error = matched_rule.message()
        fields = matched_rule.message_fields
        field = fields.get("field")

        # print(rule, field, error, fields, sep=" | ")

        wildcard_field = self._convert_field_to_wildcard_field(field)
        if wildcard_field in self.overwrite_messages:
            error = self.overwrite_messages[wildcard_field]

        combined_field = wildcard_field + "." + rule
        if combined_field in self.overwrite_messages:
            error = self.overwrite_messages[combined_field]

        for overwrite_field, overwrite_value in self.overwrite_fields.items():
            for key, value in fields.items():
                value = self._convert_field_to_wildcard_field(value)
                if overwrite_field == value:
                    fields[key] = overwrite_value

        if wildcard_field in self.overwrite_values:
            fields["values"] = self.overwrite_values[wildcard_field]["values"]

        return error.format(**fields)

    def _convert_field_to_wildcard_field(self, field) -> str:
        split_fields = str(field).split(".")
        for index, field in enumerate(split_fields):
            if field.isnumeric():
                split_fields[index] = self.FIELD_WILD_CARD

        return ".".join(split_fields)

    def _flatten_output(self, output: dict):
        for field, errors in output.items():
            if type(errors) is dict:
                self._flatten_output(errors)
                continue
            for error in errors:
                self._flat_list.append(error)

    def _get_field_value(self, field):
        value = self._input
        split_field = field.split(".")

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

    def _setup_plugins(self, plugins: List[Plugin]):
        for plugin in plugins:
            self.register_rules(plugin.rules())
