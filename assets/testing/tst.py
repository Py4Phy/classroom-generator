import pytest
import importlib
import pathlib
import sys
from io import StringIO
import subprocess
import re

# Make sure to run with Python 3 (on GitHub Actions, the default Python `python` is
# currently 'executable': '/usr/bin/python', 'version': '2.7.17 (default, Sep 30 2020, 13:38:04) \n[GCC 7.5.0]'}
# see https://github.com/actions/virtual-environments/blob/ubuntu18/20210123.1/images/linux/Ubuntu1804-README.md
# and https://github.com/actions/virtual-environments/issues/1816
PYTHON = "python3"

def assert_variable(name, value, reference, check_type=False):
    if check_type:
        # check type (exact, not isinstance)
        ref_type = type(reference)
        assert type(value) == ref_type, f"Data type of '{name}' is wrong, should be '{ref_type}'."

    try:
        assert value == pytest.approx(reference), f"{name}={value} is not correct, should have been '{reference}'."
    except TypeError:
        assert value == reference, f"{name}={value} is not correct, should have been '{reference}'."



def _test_file(p):
    p = pathlib.Path(p)
    if not p.exists():
        raise AssertionError(f"Solution file '{p}' is missing.")


def _test_variable(name, reference, mod, check_type=False):
    mod = pathlib.Path(mod)
    try:
        module = importlib.import_module(mod.stem)
    except ImportError:
        raise AssertionError(f"File '{mod}' could not be imported.")
    try:
        value = getattr(module, name)
    except AttributeError:
        raise AssertionError(f"File '{mod}' does not contain variable '{name}'.")

    assert_variable(name, value, reference, check_type=check_type)


def _test_variable_with_input(name, input_values, reference, mod, check_type=False):
    mod = pathlib.Path(mod)
    if not mod.exists():
        raise AssertionError(f"File '{mod}' could not be found")

    oldstdin = sys.stdin
    try:
        sys.stdin = StringIO("\n".join([str(s) for s in input_values]) + "\n")
        # main input() reads values
        # execute the code in __main__ and have variables in GLOBALS
        GLOBALS = {'__name__': '__main__'}
        exec(open(mod).read(), GLOBALS)
    except Exception as exc:
        raise AssertionError(f"Running {mod} failed with {exc.__class__.__name__}:\n'{exc}'\nRun locally to debug.")
    finally:
        sys.stdin = oldstdin

    try:
        value = GLOBALS[name]
    except KeyError:
        raise AssertionError(f"Solution file '{mod}' does not contain variable '{name}'.")

    assert_variable(name, value, reference, check_type=check_type)

def _test_output(filename, reference, input_values=None):
    input_values = "\n".join([str(s) for s in input_values]) + "\n" if input_values is not None else None
    output = subprocess.check_output([PYTHON, filename], input=input_values, universal_newlines=True)
    m = re.search(reference, output, flags=re.MULTILINE)
    assert m, f"'{PYTHON} {filename}': output\n\n{output}\n\ndid not match regular expression\n\n{reference}\n\n"

