# ASSIGNMENT: $assignment
# PROBLEM NUMBER: $problem

# place as problem_x/test_name.py so that relative imports work

import pytest

from ..tst import _test_function

FILENAME = '${filename}'
POINTS = ${points}

@pytest.mark.parametrize(("args", "kwargs", "reference"),
                         list(zip(${args}, ${kwargs}, ${reference})))
def test_${name}(args, kwargs, reference):
    return _test_function("${function}",
                          args,     # tuple or list
                          kwargs,   # dict
                          reference,
                          FILENAME,
                          check_type=${check_type})
