#!/usr/bin/env python
# -*- coding: utf-8 -*-

# generate tests from generate.yml

import string
import pathlib
import os.path
import shutil
import yaml
import json

# fixed directory structure
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
# └── bin
#     ├── ...
#     └── generate_tests.py

# templates for Assignments are in a repo with each
# assignment in its own subdirectory and this script uses
# the path to generate.yml at the root of the assignment dir
# to find everything else.
#
# Assignments
#     ├── ...
#     └── hw03
#         └── generate.yml


ASSETS = pathlib.Path(__file__).parent / os.path.pardir / "assets"

testing_assets_dir = ASSETS / "testing"
templatedir = testing_assets_dir / "templates"
templates = {'variable':
             string.Template((templatedir / '_test_variable.template.py').read_text()),
             'multi_variables':
             string.Template((templatedir / '_test_multi_variables.template.py').read_text()),
             'variable_with_input':
             string.Template((templatedir / '_test_variable_with_input.template.py').read_text()),
             'output':
             string.Template((templatedir / '_test_output.template.py').read_text()),
             'file':
             string.Template((templatedir / '_test_file.template.py').read_text()),
             'fileregex':
             string.Template((templatedir / '_test_fileregex.template.py').read_text()),
             'imagefile':
             string.Template((templatedir / '_test_imagefile.template.py').read_text()),
             'content':
             string.Template((templatedir / '_test_filecontent.template.py').read_text()),
             'function':
             string.Template((templatedir / '_test_function.template.py').read_text()),
             }

template_dependencies = [testing_assets_dir / "tst.py"]

# copy dict as a template, do not modify
autograder = {
    "name": None,     # replace
    "setup": "sudo -H pip3 install pytest numpy",  # default environment
    "run": "pytest --tb=line tests/test_NAME.py",  # replace tests/test_NAME.py
    "input": "",
    "output": "",
    "comparison": "included",
    "timeout": 1,
    "points": None,   # replace
    "extra": False,   # extra credit flag (requires workflow py4phy/autograding@v1.1)
}



def choose_template(problem):
    if 'test' in problem:
        # custom test under ./tests (from where generate.yml sits)
        return "tests" / pathlib.Path(problem['test'])
    elif 'output' in problem:
        return templates['output']
    elif 'content' in problem:
        return templates['content']
    elif 'file' in problem:
        return templates['file']
    elif 'fileregex' in problem:
        return templates['fileregex']
    elif 'imagefilename' in problem:
        return templates['imagefile']
    elif 'function' in problem:
        return templates['function']

    if 'variable' not in problem:
        raise ValueError(f"No template found. Not sure what to do with\n{problem}")
    # everything else requires "variable" to be defined

    if problem.get('input_values', None) is not None:
        return templates['variable_with_input']
    elif isinstance(problem['variable'], list):
        # multiple comparisons needed
        return templates['multi_variables']
    # simple: just one variable
    return templates['variable']

def make_safe_filename(filename, keepcharacters=('_')):
    # based on https://stackoverflow.com/a/7406369
    filename = filename.replace(" ", "_")
    return "".join(c for c in filename if c.isalnum() or c in keepcharacters).strip()

def create_init_file(directory, comment):
    initfile = directory / pathlib.Path("__init__.py")
    initfile.write_text(f"# {comment}\n")
    print(f"+ Created {initfile}")
    return initfile


def create_subproblem(subproblem, problem_dir,
                      build_dir,
                      topdir=pathlib.Path(os.path.curdir),
                      setup_command=autograder['setup'],
                      extra=False,
                      metadata=None,
                      pytest_args=None):
    """Build tests and metadata for a single subproblem.

    Custom tests are taken from topdir/tests, other tests are generated.

    Parameters
    ----------
    subproblem : dict
                 data structure for an entry in *problems.items*
    problem_dir: pathlib.Path
                 dest directory for the problem, relative to the root
                 (should include ``tests/...``); needs to be relative
                 to `build_dir`
    build_dir : pathlib.Path
                 directory where files are build (typically build_dir/)
    topdir : pathlib.Path
                 directory that contains "tests/" and generate.yml, default
                 is the current dir "."
    setup_command : str
                 command for installing test environment; default is
                 ``autograder['setup']``.
    extra : bool
                 declare problem to be extra credit (``True``) or required
                 (``False``). The default is ``False``. If the test itself
                 (in `subproblem`) is marked as ``extra=True`` then the
                 state is determined by ``extra or subproblem['extra']``,
                 i.e., if any of these is ``True`` then the test is marked
                 as a extra credit/bonus.

                 Use of `extra` requires the py4phy/autograding@v1.1 workflow.
    metadata : dict
                 data for the whole problem (assignment, problem, filename)
    pytest_args : str
                 additional arguments for ``pytest ... tests/problem_x/test_name.py``
                 (if not provided in subproblem, the default ``--tb=line`` is used)

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
    subs['name'] = make_safe_filename(subproblem['name'])
    extra_credit = extra or subproblem.get('extra', False)
    if extra_credit:
        print(f".. EXTRA CREDIT test because extra={extra_credit} in config.")

    subs.setdefault('check_type', False)
    subs.setdefault('relative_tolerance', None)  # use pytest.approx() defaults
    subs.setdefault('absolute_tolerance', None)  # use pytest.approx() defaults
    subs.setdefault('input_values', None)
    subs.setdefault('regex', True)
    if pytest_args is None:
        if subs.get('output', None) or subs.get('test', None):
            # show more debug output with all the pattern or custom tests
            pytest_args = "--tb=short"
        else:
            pytest_args = "--tb=line"
    subs.setdefault('pytest_args', pytest_args)
    subs.update(metadata)

    if subs['name'] != subproblem['name']:
        print(f"** NOTE: using '{subs['name']}' as testname instead of '{subproblem['name']}'")

    # function template
    if subs.get('args', None) or subs.get('kwargs', None):
        # ensure equal length of args and kwargs lists for parametrized tests
        args = subs.get('args', None)
        kwargs = subs.get('kwargs', None)
        if isinstance(args, list) and not kwargs:
            subs['kwargs'] = len(args) * [{}]
        elif isinstance(kwargs, list) and not args:
            subs['args'] = len(kwargs) * [()]
        else:
            # check
            if len(args) != len(kwargs):
                raise ValueError(f"Function args and kwargs must be lists of same length: |{args}| != |{kwargs}|")

    template = choose_template(subs)

    testfilename = f"test_{subs['name']}.py"
    testfile = build_dir / problem_dir / testfilename

    if isinstance(template, string.Template):
        print(f".. Using standard template ")
        t = template.substitute(subs)
        testfile.write_text(t)
        used_templates = True
    else:
        # custom file: just copy from the topdir/tests directory
        print(f"++ Copy custom test {topdir / template}")
        shutil.copy(topdir / template, testfile)
        used_templates = False

    print(f"++ Created {testfile}... [{subproblem['points']}]")

    # generate entry for autograding.json
    # NOTE: output and input are always "" because we use our own output checker
    ag = autograder.copy()
    ag['name'] = f"Test: Problem {problem['problem']} / {subproblem['name']}"
    ag['points'] = subproblem['points']
    ag['run'] = f"pytest {subs['pytest_args']} {problem_dir / testfilename}"
    ag['setup'] = setup_command
    # only include extra if True (maximum backwards compatibility with
    # education/autograding workflow)
    if not extra_credit:
        try:
            del ag['extra']
        except KeyError:
            pass
    else:
        ag['extra'] = extra_credit

    print(f"++ Created entry for autograder: {ag['name']}: {ag['run']}")

    return ag, used_templates

def copy_template_dependencies(test_dir):
    """copy everything in :attr:`template_dependencies` to `test_dir`"""

    for asset_path in template_dependencies:
        shutil.copy(asset_path, test_dir)
        print(f"+ Copied {asset_path} --> {test_dir} (dependency)")


def create_autograder_json(tests_list, directory):
    """write 'autograding.json' in `directory` from `tests_list` list of dicts"""

    ag_json = directory / pathlib.Path("autograding.json")
    ag_json.write_text(json.dumps({'tests': tests_list}, indent=2))

    print(f"+ Created '{ag_json}'")
    return ag_json

def copy_assets(names, dest_dir, topdir=pathlib.Path(os.curdir)):
    """Copy all entries in list names to directory dest_dir.

    Files/directories in names are looked for under topdir.
    """
    topdir = pathlib.Path(topdir)
    for name in names:
        # find assets under topdir
        asset_path = topdir / name
        if asset_path.is_dir():
            newdir = dest_dir / asset_path.parts[-1]

            # only copytree >= 3.8 has dirs_exist_ok=True so just nuke the target first...
            if newdir.absolute() == topdir.absolute():
                raise ValueError("asset '{name}' cannot be the top directory {topdir}")
            elif newdir.absolute() == dest_dir.absolute():
                raise ValueError("asset '{name}' cannot be the destination directory {dest_dir}")
            if newdir.exists():
                shutil.rmtree(newdir)
                print(f"+ Removed {newdir} to prepare for a fresh copy of asset {name}")

            shutil.copytree(asset_path, newdir, symlinks=True)
            operation = "Recursively copied"
        else:
            shutil.copy2(asset_path, dest_dir)
            operation = "Copied"
        print(f"+ {operation} custom asset {asset_path} --> {dest_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate files to be used with GitHub Classroom.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("filename", nargs="?",
                        default="generate.yml",
                        help="classroom-generator yml file")
    parser.add_argument("--build-dir", "-B",
                        metavar="DIR",
                        default="BUILD",
                        help="directory to contain the generated directory; can exist already, in "
                        "which case files will be overwritten")
    args = parser.parse_args()

    configfile = pathlib.Path(args.filename)
    topdir = configfile.parent

    cfg = yaml.load(open(configfile), Loader=yaml.FullLoader)
    problemset = cfg['problemset']

    build_dir = pathlib.Path(args.build_dir) / make_safe_filename(problemset['name'])
    build_test_dir = build_dir / "tests"
    test_dir = pathlib.Path("tests")  # relative to the build root from where pytest is invoked

    # keep output because BUILD_all.sh greps it for BUILD_DIR: ... yes, it's dirty
    print(f"assignment: {problemset['name']}")
    print(f"topdir: {topdir}")
    print(f"configfile: {configfile}")
    print(f"BUILD_DIR: {build_dir}")
    print(f"test_dir: {build_test_dir}")

    build_dir.mkdir(parents=True, exist_ok=True)
    build_test_dir.mkdir(parents=True, exist_ok=True)

    # custom global assets
    copy_assets(problemset.get('test_assets', []), build_test_dir,
                topdir=topdir / "tests")
    copy_assets(problemset.get('assets', []), build_dir,
                topdir=topdir)

    # make it a package for relative imports
    create_init_file(build_test_dir, f"tests for {problemset['name']}")

    # If we use any of the templates then we also need to copy other
    # assets. (Can be set explicitly but will automatically set to True
    # later if any templates are being used implicitly)
    used_templates = problemset.get('used_templates', False)

    # default test environment
    default_setup = problemset.get('setup', autograder['setup'])

    # becomes "tests": test_list in autograding.json
    tests_list = []

    # running total of points
    points_total = 0

    for problem in problemset.get('problems', []):
        print(f"= problem: {problem['problem']} in file '{problem.get('filename')}'")
        metadata = {'assignment': problemset['name'],
                    'problem': problem['problem'],
                    'filename': problem.get('filename', ""),
                    }

        # copy problem-specific assets
        copy_assets(problem.get('assets', []), build_dir,
                    topdir=topdir)

        problem_dir = test_dir / pathlib.Path(
            make_safe_filename(f"problem_{problem['problem']}"))
        build_problem_dir = build_dir / problem_dir
        build_problem_dir.mkdir(exist_ok=True)
        print(f"+ Created {build_problem_dir}/")

        # make it a package for relative imports
        create_init_file(build_problem_dir,
                         f"tests for {problemset['name']}: Problem {problem['problem']}")

        for subproblem in problem['items']:
            # special setup (define per problem but needs to be specified per test for autograder)
            ag, sub_used_templates = create_subproblem(subproblem, problem_dir,
                                                       build_dir,
                                                       topdir=topdir,
                                                       setup_command=problem.get('setup', default_setup),
                                                       extra=problem.get('extra', False),
                                                       metadata=metadata)
            tests_list.append(ag)
            used_templates = used_templates or sub_used_templates
            points_total += subproblem['points']

    if points_total == 0:
        print("WW WARNING: total points is ZERO: did you include a 'problemset' list?")

    # copy standard test assets if needed
    if used_templates:
        copy_template_dependencies(build_test_dir)

    create_autograder_json(tests_list, build_dir)

    print(f"* TOTAL POINTS      [{points_total}]")
