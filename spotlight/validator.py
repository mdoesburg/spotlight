from typing import Union, List

from spotlight import errors as err
from spotlight import rules as rls


class Validator:
    """
    Creates an instance of the Validator class.
    """

    class Plugin:
        """
        Creates an instance of the Validator Plugin class.
        """

        def rules(self) -> List[rls.BaseRule]:
            return []

    def __init__(self, plugins: List[Plugin] = None):
        self._output = {}
        self._flat_list = []

        self.overwrite_messages = {}
        self.overwrite_fields = {}
        self.overwrite_values = {}

        self._implicit_rules = []
        self._registered_rules = []
        self._available_rules = {}
        self._excluded_fields = []

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
    ):
        """
         Validate input with given rules.

         Parameters
         ----------
         input_ : Union[dict, object]
             Dict or object with input that needs to be validated.
             For example: {"email": "john.doe@example.com"},
             Input(email="john.doe@example.com")
         input_rules : Union[dict, object]
             Dict with validation rules for given input.
             For example: {"email": "required|email|unique:user,email"}

         """

        self._output = {}
        self._excluded_fields = []
        self._validate_input(input_, input_rules)

        if flat:
            self._flat_list = []
            self._flatten_output(self._output)

            return self._flat_list

        return self._output

    def _validate_input(self, input_: Union[dict, object], input_rules: dict):
        # Transform input to dictionary
        if not isinstance(input_, dict) and not isinstance(input_, list):
            input_ = input_.__dict__

        # Iterate over fields
        for field in input_rules:
            rules = input_rules.get(field).split("|")
            # Iterate over rules
            for rule in rules:
                # Verify that rule isn't empty
                if rule != "":
                    # Split rule name and rule_values
                    rule_name, *rule_values = rule.split(":")

                    # Check if field is validatable
                    if self._is_validatable(rule_name, field, input_):
                        # Check if rule exists
                        if rule_name in self._available_rules:
                            matched_rule = self._available_rules.get(rule_name)

                            wildcard_locations = self._get_wildcard_locations(field)

                            if len(wildcard_locations) > 0:
                                index = 0
                                while True:
                                    index_field = self._replace_character_at_index(
                                        field, index, wildcard_locations[0]
                                    )
                                    if not index_field in self._excluded_fields:
                                        try:
                                            self._validate_input_to_rule(
                                                index_field,
                                                input_,
                                                matched_rule,
                                                rule_values,
                                                rule_name,
                                            )
                                        except (IndexError, TypeError):
                                            break
                                    index = index + 1

                            elif not field in self._excluded_fields:
                                self._validate_input_to_rule(
                                    field, input_, matched_rule, rule_values, rule_name
                                )
                        else:
                            raise Exception(err.RULE_NOT_FOUND.format(rule=rule_name))

    def _validate_input_to_rule(
        self, field, input_, matched_rule, rule_values, rule_name
    ):
        # Execute correct validation method
        value = self._get_value(field, input_)

        # Rule
        if isinstance(matched_rule, rls.Rule):
            passed = matched_rule.passes(field, value)
        # Dependent Rule
        elif isinstance(matched_rule, rls.DependentRule):
            passed = matched_rule.passes(field, value, rule_values, input_)

        # If rule didn't pass, add error
        if not passed:
            self._add_error(
                rule=rule_name,
                complete_field=field,
                error=matched_rule.message(),
                fields=matched_rule.message_fields,
            )

            if matched_rule.stop:
                self._excluded_fields.append(field)

    def _is_validatable(self, rule, field, input_):
        return self._present_or_rule_is_implicit(rule, field, input_)

    def _present_or_rule_is_implicit(self, rule, field, input_):
        return self._validate_present(field, input_) or self._is_implicit(rule)

    def _validate_present(self, field, input_):
        wildcard_locations = self._get_wildcard_locations(field)
        field_list = field.split(".")
        for wildcard_location in wildcard_locations:
            field_list[wildcard_location] = "0"

        field = ".".join(field_list)

        try:
            value = self._get_value(field, input_)
            if value is None:
                return False
        except (TypeError, IndexError, KeyError):
            return False

        return True

    def _is_implicit(self, rule):
        return rule in self._implicit_rules

    def _add_error(self, rule, complete_field, error, fields=None):
        error = self._create_error(error, complete_field, fields, rule)
        if complete_field in self._output:
            self._output[complete_field].append(error)
        else:
            self._output[complete_field] = [error]

    def _create_error(self, error, complete_field, fields, rule):
        wildcard_field = self._convert_field_to_wildcard_field(complete_field)
        if wildcard_field in self.overwrite_messages:
            error = self.overwrite_messages[wildcard_field]

        combined_field = wildcard_field + "." + rule

        if combined_field in self.overwrite_messages:
            error = self.overwrite_messages[combined_field]

        for overwrite_field in self.overwrite_fields:
            for key, value in fields.items():
                value = self._convert_field_to_wildcard_field(value)
                if overwrite_field == value:
                    fields[key] = self.overwrite_fields[overwrite_field]

        if wildcard_field in self.overwrite_values:
            fields["values"] = self.overwrite_values[wildcard_field]["values"]

        return error.format(**fields)

    @staticmethod
    def _convert_field_to_wildcard_field(field):
        split_fields = str(field).split(".")
        if len(split_fields) > 1:
            for index, field in enumerate(split_fields):
                if field.isnumeric():
                    split_fields[index] = "*"

        return ".".join(split_fields)

    def _flatten_output(self, output):
        for item in output:
            if type(output[item]) == dict:
                self._flatten_output(output[item])
                continue
            for error in output[item]:
                self._flat_list.append(error)

    @staticmethod
    def _get_value(field, input_):
        value = input_
        split_field = field.split(".")
        try:
            for key in split_field:
                if not isinstance(value, dict) and not isinstance(value, list):
                    value = value.__dict__
                if key.isnumeric():
                    value = value[int(key)]
                else:
                    value = value.get(key)
        except AttributeError:
            return None

        return value

    @staticmethod
    def _get_wildcard_locations(field):
        split_fields = field.split(".")
        wildcard_locations = []

        for index, split_field in enumerate(split_fields):
            if split_field == "*":
                wildcard_locations.append(index)

        return wildcard_locations

    @staticmethod
    def _replace_character_at_index(field, character, index):
        split_field = field.split(".")
        split_field[index] = str(character)
        index_field = ".".join(split_field)

        return index_field

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
