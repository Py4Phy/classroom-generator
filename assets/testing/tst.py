# -*- coding: utf-8 -*-
import pytest
import importlib
import pathlib
import sys
from io import StringIO
import subprocess
import re

import numpy as np
import numpy.testing as nptst

# Make sure to run with Python 3: Always run pytest under Python 3.
PYTHON = sys.executable

def assert_python3():
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 6):
        raise AssertionError(f"The python version {v[0]}.{v[1]}.{v[2]} must be >= 3.6")

def assert_variable(name, value, reference, check_type=False,
                    rtol=None, atol=None):
    # process tolerance
    # remove kwargs set to `None` and let approx() decide
    # (defaults are rtol=1e-6 and atol=1e-12
    # https://docs.pytest.org/en/4.6.x/reference.html#pytest-approx); only setting one
    # changes behavior, see docs.
    tolerance = {name: tol for name, tol in (("abs", atol), ("rel", rtol)) if tol is not None}
    nptol = {name: tol for name, tol in (("atol", atol), ("rtol", rtol)) if tol is not None}

    if check_type:
        # check type (exact, not isinstance)
        ref_type = type(reference)
        assert type(value) == ref_type, f"Data type of '{name}' is wrong, should be '{ref_type}'."

    # If the output is a numpy array or a tuple containing arrays then we test them with numpy:
    # (rtol and atol work a bit differently from pytest.approx: It's like np.allclose(actual, desired, rtol, atol):
    # It compares the difference between `actual` and `desired` to ``atol + rtol * abs(desired)``.
    if isinstance(value, np.ndarray):
        nptst.assert_allclose(value, reference,
                              err_msg=f"{name}={value} is not correct, should have been '{reference}'.",
                              **nptol)
        return
    elif isinstance(value, tuple):
        if all([isinstance(elem, np.ndarray) for elem in value]):
            for ix, (x, ref) in enumerate(zip(value, reference)):
                nptst.assert_allclose(x, ref,
                                      err_msg=f"{name}[{ix}]={x} is not correct, should have been '{ref}'.",
                                      **nptol)
            return
        # not sure what to do with mixed tuples ... maybe pytest deals with them properly

    # fall back with pytest
    try:
        assert value == pytest.approx(reference, **tolerance), f"{name}={value} is not correct, should have been '{reference}'."
    except TypeError:
        assert value == reference, f"{name}={value} is not correct, should have been '{reference}'."

def import_file(mod):
    mod = pathlib.Path(mod)
    if not mod.exists():
        raise AssertionError(f"File {mod} is missing from {mod.cwd()}")
    try:
        module = importlib.import_module(mod.stem)
    except ImportError as err:
        raise AssertionError(f"File '{mod}' could not be imported in {mod.cwd()}."
                             f"\n{err.__class__.__name__}: {err}")
    return module

def get_attribute(name, mod):
    module = import_file(mod)
    try:
        attribute = getattr(module, name)
    except AttributeError:
        raise AssertionError(f"File '{mod}' does not contain variable '{name}'.")
    return attribute

def _test_file(p):
    p = pathlib.Path(p)
    if not p.exists():
        raise AssertionError(f"Solution file '{p}' is missing.")

def _test_imagefile(p):
    p = pathlib.Path(p)
    _test_file(p)
    # test loading as image
    try:
        import matplotlib.image as mpimg
    except ImportError:
        # matplotlib was not installed
        import warnings
        warnings.warn("This test requires matplotlib to be installed. Will AUTOMATICALLY PASS.")
        return
    try:
        img = mpimg.imread(str(p))
    except OSError as err:
        raise AssertionError(f"Failed to read image '{p}', error:\n"
                             f"{err.__class__.__name__}: {err}")

def _test_variable(name, reference, mod, **kwargs):
    value = get_attribute(name, mod)
    assert_variable(name, value, reference, **kwargs)


def _test_variable_with_input(name, input_values, reference, mod, **kwargs):
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

    assert_variable(name, value, reference, **kwargs)

def _test_output(filename, reference, input_values=None, regex=True):
    input_values = "\n".join([str(s) for s in input_values]) + "\n" if input_values is not None else None
    output = subprocess.check_output([PYTHON, filename], input=input_values, universal_newlines=True, encoding="utf-8")
    if regex:
        m = re.search(reference, output, flags=re.MULTILINE)
        match_pattern = "match regular expression pattern"
    else:
        m = reference in output
        match_pattern = "contain text"
    assert m, f"'{PYTHON} {filename}': output\n\n{output}\n\ndid not {match_pattern}\n\n{reference}\n\n"

def _test_function(funcname, fargs, fkwargs, reference, mod, **kwargs):
    func = get_attribute(funcname, mod)
    value = func(*fargs, **fkwargs)

    assert_variable(f"{funcname}(*{fargs}, **{fkwargs})", value, reference, **kwargs)

def _test_filecontent(filename, reference, regex=True):
    datafile = pathlib.Path(filename)
    if not datafile.exists():
        raise AssertionError(f"{datafile} is missing")

    output = datafile.read_text()

    if regex:
        m = re.search(reference, output, flags=re.MULTILINE)
        match_pattern = "match regular expression pattern"
    else:
        m = reference in output
        match_pattern = "contain text"
    assert m, f"'In file {filename}': output\n\n{output}\n\ndid not {match_pattern}\n\n{reference}\n\n"
