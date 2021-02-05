# ASSIGNMENT: $assignment
# PROBLEM NUMBER: $problem

# place as problem_x/test_name.py so that relative imports work

import pytest

from ..tst import _test_output, assert_python3

FILENAME = '${filename}'
POINTS = ${points}

def test_python3():
    assert_python3()

def test_${name}():
    return _test_output(FILENAME,
                        r"""${output}""",
                        input_values=${input_values})


