# ASSIGNMENT: $assignment
# PROBLEM NUMBER: $problem

# place as problem_x/test_name.py so that relative imports work

import pytest

from ..tst import _test_variable

FILENAME = '${filename}'
POINTS = ${points}

@pytest.mark.parametrize("varname,reference",
                         list(zip(${variable}, ${reference})))
def test_${name}(varname, reference):
    return _test_variable(varname, reference,
                          FILENAME,
                          check_type=${check_type})
