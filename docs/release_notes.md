# Release Notes

## 3.3.0
### Features
- Add `prohibited_if` rule
- Add `prohibited_unless` rule
- Add `prohibited_with` rule

## 3.2.0
### Features
- Add support for defining a rule with parameters as a tuple or a list
- Add `prohibited` rule

## 3.1.0
### Features
- Add `implicit` and `stop` flag support to function rules.

## 3.0.1
### Fixes
- The `after`, `after_or_equal`, `before`, and `before_or_equal` rules no longer raise a date time error when the dependent field/value is missing or incorrect.

## 3.0.0
### Breaking Changes
- Add support for date objects. Python date objects will now pass `date_time` validation and can be used in all date rules.

## 2.3.3
### Fixes
- Fix rule split bug when using date rules in combination with list notation 

## 2.3.2
### Fixes
- Exclude `regex` rule from param split. This fixes the `regex` rule for regular expressions that contain commas.

## 2.3.1
### Fixes
- Fix nested field lookup when determining date and format

## 2.3.0
### Features
- Add `after_or_equal` rule
- Add `before_or_equal` rule

## 2.2.1
### Fixes
- Nested values now get resolved properly for the `required_if` and `required_unless` rule

## 2.2.0
### Features
- Add support for better imports. For example, you can now do `from spotlight import Validator` instead of `from spotlight.validator import Validator`.

### Internal
- Increase test coverage to 100%

## 2.1.0
### Features
- Add support for custom validation functions

## 2.0.1
### Fixes
- Add missing empty checks to the `required_if`, `required_unless`, `required_with`, and `required_without` rules. These rules were only checking if a field was present instead of also checking if the value was empty or not.

## 2.0.0
### Breaking Changes
- `True` and `False` are now considered valid integers, because bool is an instance of int in Python.

## 1.1.0
### Features
- Add `regex` rule
- Add decimal support to `size` rule