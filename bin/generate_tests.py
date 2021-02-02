#!/usr/bin/env python
# -*- coding: utf-8 -*-

# generate tests from generate.yml

import string
import pathlib
import os.path
import shutil
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
# ├── Assignments
# │   ├── ...
# │   └── hw03
# │       └── generate.yml
# └── bin
#     ├── ...
#     └── generate_tests.py

ASSETS = pathlib.Path(__file__).parent / os.path.pardir / "assets"

testing_assets_dir = ASSETS / "testing"
templatedir = testing_assets_dir / "templates"
templates = {'variable':
             string.Template((templatedir / '_test_variable.template.py').read_text()),
             'multi_variables':
             string.Template((templatedir / '_test_multi_variables.template.py').read_text()),
             'variable_with_input':
             string.Template((templatedir / '_test_variable_with_input.template.py').read_text()),
             }

template_dependencies = [testing_assets_dir / "tst.py"]

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
    if 'test' in problem:
        # custom test under ./tests (from where generate.yml sits)
        return "tests" / pathlib.Path(problem['test'])

    if 'variable' not in problem:
        raise ValueError("Only templates with variable checks implemented")

    if 'input_values' in problem:
        return templates['variable_with_input']
    if isinstance(problem['variable'], list):
        # multiple comparisons needed
        return templates['multi_variables']
    # simple: just one variable
    return templates['variable']

def make_safe_filename(filename, keepcharacters=('.', '-', '_')):
    # based on https://stackoverflow.com/a/7406369
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).strip()

def create_init_file(directory, comment):
    initfile = directory / pathlib.Path("__init__.py")
    initfile.write_text(f"# {comment}\n")
    print(f"+ Created {initfile}")
    return initfile


def create_subproblem(subproblem, problem_dir, metadata=None,
                      pytest_args="--tb=line"):
    """Build tests and metadata for a single subproblem.

    Parameters
    ----------
    subproblem : dict
                 data structure for an entry in *problems.items*
    problem_dir: pathlib.Path
                 directory for the problem under ``tests``
    metadata : dict
                 data for the whole problem (assignment, problem, filename)
    pytest_args : str
                 additional arguments for ``pytest ... tests/problem_x/test_name.py``

    Returns
    -------
    ag : dict
         entry for ``autograding.yml`` for this test
    used_templates : bool
         ``True`` if any of the test templates were used, ``False`` if only custom
         test files were copied

    """
    metadata = metadata if metadata is not None else {'assignment': "HOMEWORK", 'problem': 0, 'filename': None}

    print(f"== subproblem: {subproblem['name']}  points: {subproblem['points']}")
    subs = subproblem.copy()
    subs.setdefault('check_type', False)
    subs.update(metadata)
    template = choose_template(subs)

    testfile = problem_dir / f"test_{subproblem['name']}.py"
    if isinstance(template, string.Template):
        print(f".. Using standard template ")
        t = template.substitute(subs)
        testfile.write_text(t)
        used_templates = True
    else:
        # custom file: just copy
        print(f".. Copy custom test {template}")
        shutil.copy(template, testfile)
        used_templates = False

    print(f"++ Created {testfile}... [{subproblem['points']}]")

    # generate entry for autograding.json
    ag = autograder.copy()
    ag['name'] = f"Test: Problem {problem['problem']} / {subproblem['name']}"
    ag['points'] = subproblem['points']
    ag['run'] = f"pytest {pytest_args} {'tests' / testfile}"

    print(f"++ Created entry for autograder.")

    return ag, used_templates

def copy_template_dependencies(test_dir):
    """copy everything in :attr:`template_dependencies` to `test_dir`"""

    for asset_path in template_dependencies:
        shutil.copy(asset_path, test_dir)
        print(f"+ Copied {asset_path} --> {test_dir} (dependency)")


def create_autograder_json(tests_list, directory):
    """write 'autograding.json' in `directory` from `tests_list` list of dicts"""

    ag_json = directory / pathlib.Path("autograding.json")
    ag_json.write_text(json.dumps({'tests': tests_list}))

    print(f"+ Created '{ag_json}'")
    return ag_json


if __name__ == "__main__":

    filename = "generate.yml"

    solution = yaml.load(open(filename), Loader=yaml.FullLoader)
    problemset = solution['problemset']

    build_dir = pathlib.Path("BUILD") / make_safe_filename(problemset['name'])
    test_dir = build_dir / "tests"

    print(f"assignment: {problemset['name']}")
    print(f"BUILD_DIR: {build_dir}")
    print(f"test_dir: {test_dir}")

    build_dir.mkdir(parents=True, exist_ok=True)
    test_dir.mkdir(parents=True, exist_ok=True)

    # custom global assets
    for filename in problemset.get('test_assets', []):
        # find test assets under tests/
        asset_path = "tests" / pathlib.Path(filename)
        shutil.copy(asset_path, test_dir)
        print(f"+ Copied {asset_path} --> {test_dir}")

    # make it a package for relative imports
    create_init_file(test_dir, f"tests for {problemset['name']}")

    # If we use any of the templates then we also need to copy other
    # assets.
    used_templates = False

    # becomes "tests": test_list in autograding.json
    tests_list = []

    # running total of points
    points_total = 0

    for problem in problemset['problems']:
        print(f"= problem: {problem['problem']} in file '{problem['filename']}'")
        metadata = {'assignment': problemset['name'],
                    'problem': problem['problem'],
                    'filename': problem['filename'],
                    }
        problem_dir = test_dir / pathlib.Path(f"problem_{problem['problem']}")
        problem_dir.mkdir(exist_ok=True)
        print(f"+ Created {problem_dir}/")

        # make it a package for relative imports
        create_init_file(problem_dir,
                         f"tests for {problemset['name']}: Problem {problem['problem']}")

        for subproblem in problem['items']:
            ag, sub_used_templates = create_subproblem(subproblem, problem_dir, metadata=metadata)
            tests_list.append(ag)
            used_templates = used_templates or sub_used_templates
            points_total += subproblem['points']

    # copy standard test assets if needed
    if used_templates:
        copy_template_dependencies(test_dir)

    create_autograder_json(tests_list, build_dir)

    print(f"* TOTAL POINTS      [{points_total}]")
