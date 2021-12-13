# Release Notes

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