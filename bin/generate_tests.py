#!/usr/bin/env python
# -*- coding: utf-8 -*-

# generate tests from solution.yml

import string
import pathlib
import os.path
import yaml
import json

# fixed diretcory structure
# .
# ├── README.md
# ├── assets
# │   ├── testing
# │   │   ├── templates
# │   │   │   ├── ...
# │   │   │   ├── _test_multi_variables.template.py
# │   │   │   ├── _test_variable.template.py
# │   │   │   └── _test_variable_with_input.template.py
# │   │   └── tst.py
# │   └── workflows
# │       └── classroom.yml
# ├── assignments
# │   ├── ...
# │   └── hw03
# │       └── solution.yml
# └── bin
#     ├── ...
#     └── generate_tests.py

ASSETS = pathlib.Path(__file__).parent / os.path.pardir / "assets"

templatedir = ASSETS / "testing" / "templates"
templates = {'variable':
             string.Template((templatedir / '_test_variable.template.py').read_text()),
             'multi_variables':
             string.Template((templatedir / '_test_multi_variables.template.py').read_text()),
             'variable_with_input':
             string.Template((templatedir / '_test_variable_with_input.template.py').read_text()),
             }

autograder = {
    "name": None,     # replace
    "setup": "sudo -H pip3 install pytest",
    "run": "pytest --tb=line tests/test_NAME.py",  # replace tests/test_NAME.py
    "input": "",
    "output": "",
    "comparison": "included",
    "timeout": 1,
    "points": 3    # replace
}



def choose_template(problem):
    if 'variable' not in problem:
        raise ValueError("Only templates with variable checks implemented")
    if 'input_values' in problem:
        return templates['variable_with_input']
    if isinstance(problem['variable'], list):
        # multiple comparisons needed
        return templates['multi_variables']
    # simple: just one variable
    return templates['variable']

# def stringify_dict(d):
#     return {k:str(v) for k,v in d.items()}

if __name__ == "__main__":

    filename = "solution.yml"

    solution = yaml.load(open(filename))
    problemset = solution['problemset']

    tests_list = []  # becomes "tests": test_list in autograding.json
    points_total = 0

    print(f"assignment: {problemset['name']}")

    for problem in problemset['problems']:
        print(f"= problem: {problem['problem']} in '{problem['filename']}'")
        metadata = {'assignment': problemset['name'],
                    'problem': problem['problem'],
                    'filename': problem['filename'],
                    }
        problem_dir = pathlib.Path(f"problem_{problem['problem']}")
        problem_dir.mkdir(exist_ok=True)
        print(f"+ Created {problem_dir}/")

        # make it a package for relative imports
        initfile = problem_dir / "__init__.py"
        with open(initfile, "w") as out:
            out.write(f"# tests for {problemset['name']}: Problem {problem['problem']}\n")

        print(f"+ Created {initfile}")


        for subproblem in problem['items']:
            print(f"== subproblem: {subproblem['name']}  points: {subproblem['points']}")
            subs = subproblem.copy()
            subs.setdefault('check_type', False)
            subs.update(metadata)
            template = choose_template(subs)
            t = template.substitute(subs)
            #print(t)

            testfile = problem_dir / f"test_{subproblem['name']}.py"
            with open(testfile, 'w') as out:
                out.write(t)

            print(f"++ Created {testfile}... [{subproblem['points']}]")

            # generate entry for autograding.json
            ag = autograder.copy()
            ag['name'] = f"Test: Problem {problem['problem']} / {subproblem['name']}"
            ag['points'] = subproblem['points']
            ag['run'] = f"pytest --tb=line {'tests' / testfile}"

            tests_list.append(ag)
            print(f"++ Created entry for autograder.")

            points_total += subproblem['points']

    # write autograder json
    ag_json = pathlib.Path("autograding.json")
    ag_json.write_text(json.dumps({'tests': tests_list}))

    print(f"+ Created '{ag_json}'... [TOTAL {points_total}]")
