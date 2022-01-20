# Test generator for GitHub Classroom autograding

Homework tests are generated from templates and a `generate.yml` file
that contains the individual tests with points. The
`generate_tests.py` script then creates

- the appropriate tests themselves
- the `autograding.json` configuration for the `.github/workflows/classroom/autograding.json`

The `generate.yml` file contains data for problems with their individual
tests. For each problem, a subdirectory is made under `tests/`. Each test
gets its own test file, point value, and entry in `autograding.yml`.

At the moment the following is supported:
- template tests for checking fixed variables
- template tests for running a script with `input()` from stdin that sets variables
- template test for comparing output against regular expression
- template test for checking existence of an image file
- template test for checking existence of a file
- template test for multiline regular expression match for file content
- template test for function evaluation (parametrized, always provide args/kwargs/references as a list of lists or list of dicts)
- custom test files

All code and files are made available under the terms of the [GNU
General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Usage

Primitive at the moment... will create the new HW in a subdirectory
`BUILD/<name>` with a repository that can pushed to new repo on GitHub.

### Assignment

Create the `assignment.md` with instructions for students

Make sure to include the points banner.

### Starter code

Create any starter code.

Currently, the `BUILD_all.sh` script only copies `*.py` and `*.ipynb` files at the top level.

### Simple usage

Run the `BUILD_all.sh` script as

```bash
BUILD_all.sh -B /tmp/BUILD hw00/generate.yml
```

where `-B` is the path to where you want the final repository with
tests to show up under and the argument is the path to the
configuration yml file.

The shell script

1. calls `generate_tests.py  -B $BUILD generate.yml`
2. copies files to the final destination directory
3. initializes a git repo there and/or commits changes

You can then push the repo to a remote repository that can be used as
a template for GitHub Classroom.

### Only generating tests

The `generate_tests.py` script can be also run separately, e.g., for
testing.

Tests are generated in the BUILD directory, typically `BUILD/<name>`
where `<name>` is generated from the assignment title in
**problemset.name** in the `generate.yml` file (after making the name
"shell"-safe); we will refer to it as `$BUILD`.

```
generate_tests.py -B $BUILD path/to/hw00/generate.yml
```

See [below](#input-file) for notes on `generate.yml`

All necessary files are copied into the `$BUILD` directory. 

### Notes on BUILD_all

The `BUILD_all.sh` script does the following:

- copy `assignment.md` to `$BUILD` and symlink as `README.md`
- copy assignment assets to `$BUILD`
- `mkdir $BUILD/.github/{workflows,classroom}`
- copy `classroom.json` (static): `cp $ASSETS/workflows/classroom.yml
  $BUILD/.github/workflows` (does not change)
- copy `autograding.json` (created): `cp autograding.json
  $BUILD/.github/classroom` (is specific for this assignment)
- create `.gitignore`
- create a *template* repository for the HWxx (which is updated on
  further runs of `BUILD_all.sh`); push the repo to a bare GitHub repo
  to create an assignment template that can be used with GitHub
  Classroom.


## Input file

The input file is always called **generate.yml**.

Look at existing ones for examples. Example with common usage:

```yaml
problemset:
  name: HW example
  test_assets: ["conftest.py", "base.py"]
  used_templates: True
  setup: 'sudo -H pip3 install pytest numpy matplotlib'
  problems:
  - problem: 1
    title: Copy, rename, delete
    filename: "PHY494/"
    setup: 'sudo -H pip3 install pytest numpy'
    items:
    - name: top_dir
      points: 1
      test: test_top_dir.py
    - name: top_all_dirs
      points: 4
      test: test_all_dirs.py
  - problem: 2
    title: Hello World
    filename: "hello.py"
    items:
    - name: print_output
      points: 3
      output: 'Hello World!'
      pytest_args: '--tb=short'
  - problem: 3
    title: Data types
    filename: datatypes.py
    items:
    - name: string
      points: 1
      variable: a
      reference: "'42'"
      check_type: True
    - name: list
      points: 1
      variable: g
      reference: [3, 2, 1, 0, "lift off"]
      check_type: True
  - problem: 4
    title: Kinetic energy calculator
    filename: KEcalc.py
    items:
    - name: KEcalc
      points: 5
      variable: KE_kJ
      input_values: [8.2, 10]
      reference: 0.41
  - problem: 5
    title: Indexing lists
    filename: list_slicing.py
    items:
    - name: slice_3d
      points: 2
      variable: ['d0', 'd1', 'd2start' ,'d2stop']
      reference: [0, 1, 2, 4]
  - problem: 1
    title: Create functions
    filename: myfuncs.py
    setup: 'sudo -H pip3 install pytest numpy'
    items:
    - name: heaviside
      points: 4
      function: heaviside
      args:  [[0], [-1.e+100], [42.1], [1.2e-24], [10], [-10]]
      reference: [0.5, 0, 1., 1., 1., 0]
    - name: area_kwargs
      points: 4
      function: area
      args:  [[2, 4], [2, 4], [1, 1]]
      kwargs: [{}, {'scale': 2}, {'scale': 0.5}] 
      reference: [8, 16, 0.5]      
  - problem: 4
    title: Plot functions
    filename: myfuncs.py
    items:
    - name: heaviside
      points: 4
      function: heaviside
      args:  [[0], [-1.e+100], [42.1], [1.2e-24], [10], [-10]]
      reference: [0.5, 0, 1., 1., 1., 0]
      relative_tolerance: 1.e-6
      absolute_tolerance: 1.e-12
    - name: plot
      points: 1
      imagefilename: "heaviside.png"
    - name: discussion of plot
      points: 1
      file: "discussion.txt"
  - problem: 4b
    title: discussion
    filename: discussion.txt
    - name: mention energy conservation
      points: 1
      content: |
         \s*energy\s*conservation

``` 
          
### General notes

* starter code `*.py`, assignment sheet (`*.{pdf,md}`) must be in the
  top assignment directory

* be careful about how yaml interprets data; for instance,
  scientific/engineering notation is only understood when a decimal
  point is included an a sign after 'e': 1.e+1 (good), 1e+1 (bad),
  1.e1 (bad) --- the bad cases are interpreted as *strings*

### Keys in generate.yml

* **name** key: will be rewritten to a Python/filename-safe form
  (spaces to underscores, most weird characters stripped); will be
  used to name tests

* **test_assets**: list of files in the local `tests/` that should be
  copied; by default, only tests that are named in a **test:** key are
  copied.
  
* **used_templates:** *Normally omitted*; explicitly indicate with
  `True` that the testing infrastructure files (e.g., `tst.py`) should
  be copied even though no autogenerated tests are included. If any
  autogenerated tests are part of this assignment then a `False` will
  be automatically overriden. This flag is useful when custom tests
  import testing framework, e.g.
  ```python
  from ..tst import get_attribute, import_module
  ```
  Note that the testing infrastructure module (`tst.py`) requires 
  the `numpy` package so it should normally be included in a custom
  **setup** keyword.
* **setup**: Complete command to install the environment; **setup** at
  the top level is the default for individual **problem**
  instances. **setup** inside a **problem** overrides the global
  default.
  
  If **setup** is not provide, it defaults to `"sudo -H pip3 install
  pytest numpy"`.

* **problem** key: will be used to generate directory names

* **filename** key: this filename will be used for all autogenerated
  tests in the test **items** list. Custom tests (**test**) can test
  another filename.

* **items**: each entry in this list is an independent test run, which
  runs in a fresh environment, and counts as a separate test for the
  autograder.

* **points**: Each test has a **points** value. A failed test is 0
  points, a passed test accrues the points value.

* **test** key: custom tests must be stored in the assignment
  directory under `tests/`. Many tests are generated from templates
  and do not need to be included (see **variable**, **output**,
  **function**)

* **variable** key: Check the value of the variable in **filename**
  after running (actually: importing) the file.

  With **check_type** (True | False) can also check the type.

* **output** key: Run the code as `python3 filename` and match the
  string in the standard output. By default, this is a *regular
  expression*.

  Can be turned into a bare string with **regular_expression** False.

  Be aware of how to structure blocks in yml (e.g., `>` for folded,
  `|` for indented blocks, and `|3` for indented with 3 whitspace
  (e.g., when first line is indented compared to following lines).

* **input_values** key: input to be read from standard input. Each
  element of the list is turned into a string and supplied with a
  newline.

* **file**: name of a file that should have been submitted;
  the test only checks that the file exists.

* **imagefilename**: name of a file that should have been submitted;
  the test only checks that the file exists and that it can be loaded
  as an image with `matplotlib.image.imread()`.
  
* **content**: multiline regular expression (like **output**) but
  matches the *content* of **filename**.

* **function:** key: functions are *always tested with parametrized
  fixtures*, i.e., arguments **args**/**kwargs** must *always* be
  present in a list in the yaml generate file

  Functions are always called with `func(*args, **kwargs)` for each
  parameter set.

  The list of **reference** values must have the same length as the
  **args** and **kwargs** lists, with one reference for each input.

  Only one of **args** or **kwargs** need to be provided; the other is
  generated with empty content if necessary.

* **relative_tolerance** and **absolute_tolerance**: set the tolerance
  values `rel` and/or `abs` for
  [pytest.approx()](https://docs.pytest.org/en/4.6.x/reference.html#pytest-approx)
  for any test that checks for floating point numbers (**variable**
  and **function**). By default they are set to `None` so that the
  pytest defaults of `rel=1e-6` and `abs=1e-12` are used. Note that
  only setting either **relative_tolerance** _or_
  **absolute_tolerance** leads to different behavior of
  `pytest.approx()`, as described in the docs. Leaving these values
  unset should be fine in most cases.



## Directory layout

### classroom-generator

The class-room generator needs the following fixed directory structure
to find assets (relative to the `bin` directory):

```
.
├── README.md
├── assets
│   ├── testing
│   │   ├── templates
│   │   │   ├── ...
│   │   │   ├── _test_multi_variables.template.py
│   │   │   ├── _test_variable.template.py
│   │   │   └── _test_variable_with_input.template.py
│   │   └── tst.py
│   └── workflows
│       └── classroom.yml
└── bin
    ├── BUILD_all.sh
    └── generate_tests.py
```

### Assignments

Assignments are stored separately but also need to have a fixed
layout:

```
hw00/
├── README.md
├── Solution
│   ├── hello.py
│   └── planets
│       └── iceplanets
│           └── hoth.txt
├── assignment_00.md
├── generate.yml
├── hello.py
└── tests
	├── test_files_and_directories.py
	└── test_helloworld.py
```

- The `generate.yml` file is the config file and drives the
  classroom-generator script `generate_tests.py`.

  It defines the top level directory for an assignment.
  
- The `tests` directory *must* be in the top directory. It contains
  custom tests that will be copied into the full problem directory.

- Starter code such as `hello.py`  is put in the top
  directory.
  
- Add a `README.md` file that will be displayed when browsing the
  repository. It should contain the badges that show points:
  
  ```markdown
  [![GitHub Classroom Workflow](../../workflows/GitHub%20Classroom%20Workflow/badge.svg?branch=main)](../../actions/workflows/classroom.yml) ![Points badge](../../blob/badges/.github/badges/points.svg)
  ```
  
- Add additional documents (as .md or .pdf files) to describe the
  task.
  
- Keep solutions in a `Solution` directory for reference. They are not
  used anywhere. The `generate.yml` file needs to either contain the
  correct reference values or the custom tests need to contain the
  code to check for correctness.
  
  **Keep assignment template repositories private if they contain
  solutions.**
  

## TODO
- documentation
