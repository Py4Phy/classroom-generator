# Test generator for GitHub Classroom autograding

*classroom-generator* builds template repositories for [GitHub
Classroom](https://classroom.github.com/) assignments.

Homework tests are generated from templates and a `generate.yml` file
that contains the individual tests with points. The
`generate_tests.py` script then creates

- the appropriate tests themselves
- the `autograding.json` configuration for the
  `.github/workflows/classroom/autograding.json`
  (The [py4phy/autograding@v1.1](https://github.com/Py4Phy/autograding)
  workflow is used; this is a fork of
  [stevenbitner/autograding](https://github.com/stevenbitner/autograding),
  @stevenbitner 's updated version of the original GitHub
  [education/autograding](https://github.com/education/autograding) workflow)

The `generate.yml` file contains data for problems with their individual
tests. For each problem, a subdirectory is made under `tests/`. Each test
gets its own test file, point value, and entry in `autograding.yml`.

At the moment the following is supported:
- template tests for checking fixed variables
- template tests for running a script with `input()` from stdin that sets variables
- template test for comparing output against regular expression
- template test for checking existence of an image file
- template test for checking existence of a file
- template test for checking existence of at least one file matching a regular expression
- template test for multiline regular expression match for file content
- template test for function evaluation (parametrized, always provide args/kwargs/references as a list of lists or list of dicts)
- custom test files

A hacky `BUILD_all.sh` script is provided to bundle the generated
tests, assets, and GitHub workflow into a repository that can be
immediately pushed to an empty template repository on GitHub.

All code and files are made available under the terms of the [GNU
General Public License v3](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Tutorial

In this mini-tutorial we will create a Classroom assignment for simple in-class
exercises with NumPy and matplotlib. All materials are publicly
available at https://github.com/Py4Phy .

We will use
[Py4Phy/activity_04_source](https://github.com/Py4Phy/activity_04_source)
as input (normally, students would likely not see this repository
because I am including the solutions there). The generated template
repository with the files for the GitHub actions autograding workflow
is
[Py4Phy/Activity_04_numpy_and_matplotlib](https://github.com/Py4Phy/Activity_04_numpy_and_matplotlib).


### Get classroom-generator
You need a Python environment with the pyyaml package included.

Currently, no real installation is provided. Just clone the repo:
```
git clone https://github.com/Py4Phy/classroom-generator.git
```
Then use the scripts in the `classroom-generator/bin` directory.

### Get the example sources
Clone the
[Py4Phy/activity_04_source](https://github.com/Py4Phy/activity_04_source)
repository:

```
git clone https://github.com/Py4Phy/activity_04_source.git
```

### Create the template repository for GitHub Classroom

We first build the template locally in a directory `templates`:
```
mkdir templates
```
Run classroom-generator's `BUILD_all.sh` script:
```
./classroom-generator/bin/BUILD_all.sh -B templates/activity_04_numpy/generate.yml
```

The new template repo is created as
**templates/Activity_04_numpy_and_matplotlib**. During this process,
files are copied and new tests are created. An input file for the
autograding workflow is generated and moved to the right
place. Finally, everything is turned into a local git repository and
checked in. Note that running the process again  will add commits to
the repo (if anything changed).

### Push template repo to GitHub

Now **create a new repository on GitHub named
Activity_04_numpy_and_matplotlib** under YOURORG or YOURNAME.

Push changes from the **local** Activity_04_numpy_and_matplotlib.git
repo to the remote:
```
git remote add origin git@github.com:YOURORG/Activity_04_numpy_and_matplotlib.git
git branch -M main
git push -u origin main
```

**Set the remote to be a template** under the Settings. (IMPORTANT:
Otherwise GitHub Classroom cannot use it!)

Your remote template repository should look like
[Py4Phy/Activity_04_numpy_and_matplotlib](https://github.com/Py4Phy/Activity_04_numpy_and_matplotlib).


### Set up an assignment in Classroom
In [GitHub Classroom](classroom.github.com/) create a **New
Assignment** with the following settings:

* Assignment basics
  * Assignment Title: *activity-04* (or whatever you want to call it)
  * Deadline: (choose one if you like)
  * Individual or group assignment: Individual assignment
  * Repository visibility: *Private*
  * Grant students admin access to their repository: no (recommended,
    but your choice)
* Starter code and environment
  * Add a template repository to give students starter code:
    **YOURORG/Activity_04_numpy_and_matplotlib**
  * Add a supported editor: (your choice)	
* Grading and feedback
  * Add autograding tests: **leave empty** (do NOT add tests here as
    this will overwrite your generated configuration!)
  * Enable feedback pull requests: (your choice)
  
Then **Create assignment**.

Distribute the magic link to your students.



## Usage

Primitive at the moment... 

```bash
./classroom-generator/bin/BUILD_all.sh -B ./template_assignments hw02/generate.yml
```

where `hw02/` contains the configuration, starter code, and problem
description. A template repository is then created under
`./template_assignments/HW_02`.

## Example

Example layout for `hw02`:

    hw02/
    ├── README.md                        <----- documentation
    ├── Solution                         <----- solution files
    │   ├── hello.py                            (not distributed)
    │   └── planets
    │       └── iceplanets
    │           └── hoth.txt
    ├── assignment.md                     <----- problem description
    ├── generate.yml                      <----- configuration file
    ├── hello.py                          <----- starter code
    └── tests                             <----- custom tests
        ├── test_files_and_directories.py
        └── test_helloworld.py

The `generate.yml` file contains

```yaml
problemset:
  name: HW 02
  assets: ["README.md", "assignment.md"]
  problems:
  - problem: 1
    title: Hello World
    filename: "hello.py"
    assets: ["hello.py"]
    items:
    - name: print_output
      points: 3
      output: 'Hello World!'
      pytest_args: '--tb=short'
    - name: run_program
      points: 2
      test: test_helloworld.py
  - problem: 2
    title: Directories and Files
    setup: "sudo -H pip3 install pytest"
    filename: "planets/"
    items:
    - name: tree_structure
      points: 5
      test: test_files_and_directories.py
```

Example layout of the generated `HW_02` template directory (it's named
`HW_02` because the key `problemset.name: HW 02` was made
filepath-safe and used as a name):

    HW_02/
    ├── .github                         <--- GitHub autograding workflow
    │   ├── classroom
    │   │   └── autograding.json
    │   └── workflows
    │       └── classroom.yml
    ├── .gitignore
    ├── README.md                       <--- documentation
    ├── assignment.md                   <--- problem description
    ├── hello.py                        <--- starter code
    └── tests                           <--- tests for pytest
        ├── __init__.py
        ├── problem_1
        │   ├── __init__.py
        │   ├── test_print_output.py    <--- generated "output" test
        │   └── test_run_program.py     <--- custom test (test_helloworld.py)
        ├── problem_2
        │   ├── __init__.py
        │   └── test_tree_structure.py  <--- custom test (test_files_and_directories.py)
        └── tst.py                      <--- test framework asset


## Documentation

* Include `README.md` with points banner and generic
  instructions. (Can be nearly identical between assignments.)
* Create the `assignment.md` or `assignment.pdf` with instructions for
  students. If in markdown or restructured text, also include the
  points banner.
  
### Configuration

Include *any* docs into **assets** in the `generate.yml` file (namely,
in the `problemset.assets` key at the top) so that they get copied.

Example:
```yaml
assets: ["README.md", "assignment_00.md"]
```

### Points banner 

Make sure to include the **points banner** that updates with the
currently achieved points and the status of the tests:

  ```markdown
  [![GitHub Classroom Workflow](../../workflows/GitHub%20Classroom%20Workflow/badge.svg?branch=main)](../../actions/workflows/classroom.yml) ![Points badge](../../blob/badges/.github/badges/points.svg)
  ```

The banner is the same for all assignments. Clicking the *GitHub
Classroom Workflow* status badge links to the Action so that students
can read the test feedback from the autograding step.



## Starter code

Create any starter code that students need. Files are copied
verbatim. Whole directories can also be copied.

### Configuration

Include any starter code filenames or directory names in the
**problem.assets**.

For example:
```yaml
  - problem: 2
    title: Hello World
    assets: ["hello.py"]
```

Note that **assets** is always a list, even if you only have one
file. Directory names can be terminated with a slash but that is not
necessary.

## Building the template repository
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
2. copies static files to the final destination directory
3. creates the specific workflow for GitHub 
4. initializes a git repo there and/or commits changes

You can then push the repo to a remote repository that can be used as
a template for GitHub Classroom.

### Only generating tests

The `generate_tests.py` script can be also run separately, e.g., for
testing.

Tests are generated in the BUILD_DIR directory, typically `BUILD/<name>`
where `<name>` is generated from the assignment title in
**problemset.name** in the `generate.yml` file (after making the name
"shell"-safe); we will refer to it as `$BUILD`.

```
generate_tests.py -B BUILD_DIR  path/to/hw00/generate.yml
```

See [below](#input-file) for notes on `generate.yml`

All necessary files are copied into the `$BUILD` directory. 

### Notes on BUILD_all

The `BUILD_all.sh` script does the following:

- runs `generate_tests.py -B BUILD_DIR generate.yml`
- `mkdir $BUILD/.github/{workflows,classroom}`
- copy `classroom.json` (static): `cp $ASSETS/workflows/classroom.yml
  $BUILD/.github/workflows` (does not change)
- copy `autograding.json` (created): `cp autograding.json
  $BUILD/.github/classroom` (is specific for this assignment)
- create `.gitignore`
- create a *template* repository for the HWxx (which is updated on
  further runs of `BUILD_all.sh`)
  
  (Manually push the repo to a bare GitHub repo to create an
  assignment template that can be used with GitHub Classroom.)


## Configuration file

The configuration file is in YAML format and is conventionally called
**generate.yml** (but can in principle be called anything).

Example with common usage (the keys are explained below):

```yaml
problemset:
  name: HW example
  test_assets: ["conftest.py", "base.py"]
  assets: ["README.md", "assignment.pdf"]
  used_templates: True
  setup: 'sudo -H pip3 install pytest numpy matplotlib'
  problems:
  - problem: 1
    title: Copy, rename, delete
    filename: "PHY494/"
    assets: ["PHY494/"]
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
    assets: ["datatypes.py", "xmodule.py"]
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
    assets: ["graph.png", "data.csv"]
    - name: mention energy conservation
      points: 1
      content: |
         \s*energy\s*conservation
  - problem: 5
    title: data analysis (BONUS)
    extra: True
    - name: produce numbered data files
      points: 3
      fileregex: "datafiles/data_\d+\.(dat|csv)"

``` 
          
### General notes

* Starter code `*.py`, assignment sheet (`*.{pdf,md}`) etc are copied
  *to the top* of the template directory; if you want directory trees,
  put them in a directory and list the directory in **assets** because
  trees are copied as-is.

* Be careful about how yaml interprets data; for instance,
  scientific/engineering notation is only understood when a decimal
  point is included an a sign after 'e': 1.e+1 (good), 1e+1 (bad),
  1.e1 (bad) --- the bad cases are interpreted as *strings*. See the
  [pyyaml documentation](https://pyyaml.org/wiki/PyYAMLDocumentation).

### Keys in `generate.yml`

#### General

Keys at the top level (problemset)

* **name** key: will be rewritten to a Python/filename-safe form
  (spaces to underscores, most weird characters stripped); will be
  used to name tests and the $BUILD directory

* **test_assets**: list of files in the local `tests/` that should be
  copied; by default, only tests that are named in a **test:** key are
  copied. This is useful to copy additional files such as
  `conftest.py` for global fixtures.
  
* **used_templates:** *Normally omitted*; explicitly indicate with
  `True` that the testing infrastructure files (e.g., `tst.py`) should
  be copied even though no autogenerated tests are included. If any
  autogenerated tests are part of this assignment then a `False` will
  be automatically overriden. This flag is useful when custom tests
  import testing framework, e.g.
  
  ```python
  from ..tst import get_attribute, import_module
  ```
  
  Note that the testing infrastructure module (`tst.py`) requires the
  `numpy` package so installation of `numpy` should normally be
  included in a custom **setup** keyword.
* **setup**: Complete command to install the environment; **setup** at
  the top level is the default for individual **problem**
  instances. **setup** inside a **problem** overrides the global
  default.
  
  If **setup** is not provided, it defaults to `"sudo -H pip3 install
  pytest numpy"`.


#### Problem

Each problem contains one or more tests.

* **problem** key: will be used to generate directory names

* **title** key: name of the problem

* **filename** key: this filename will be used for all autogenerated
  tests in the test **items** list that require a filename as
  input. Custom tests (**test**) can test another filename.
  
 * **assets** key: list of files and/or directories that will be
  copied to the assignment (e.g., starter code, data, ...). Only list
  top level files/directories. Sub-paths such as "problem_1/data.csv"
  would just copy "data.csv" to the top level. Instead copy
  "problem_1/" (trailing slash is ignored by `shutil.copytree`).
  The **assets** can be listed at the **problemset** (top) level and the
  **problem** level (q.v.).
  
* **setup**: Complete command to install the environment for this
  problem only. (Packages are only downloaded once so installing a new
  environment is fast.)

* **items**: each entry in this list is an independent test run, which
  runs in a fresh environment, and counts as a separate test for the
  autograder.

* **extra**: Set to `True` if this problem counts as extra credit (or
  bonus). The default is `False`. Points for extra credit are
  accrued but the total is listed as the sum of points without any
  extra credit. The green *passing* badge is added as soon as the
  regular point total is reached.
  
  Using this flag requires the special
  [py4phy/autograding@v1.1](https://github.com/Py4Phy/autograding)
  workflow.

#### Individual tests

The philosophy is to have one test per property that is to be tested.

* **name**: name of the test (will be made Python-safe and used for
  naming the generated test file) 

* **points**: Each test has a **points** value. A failed test is 0
  points, a passed test accrues the points value.
  
  Test that are part of problems with **extra:** `True` can fail/pass
  as usual but the **points** are *not* included in the point total for
  the full problem set.

* **extra**: Set to `True` if this test counts as extra credit (or
  bonus). The default is `False`. See the notes on **extra** for the
  whole problem.
  
  The values of **extra** at the problem and the test level are
  combined with logical `or` so that if *any* of them are set to
  `True` then the test will count as extra credit.


##### Available tests

Each test item should contain exactly one of the follwing keys that
determines how code is being tested.  Many tests are generated from
templates and do not need to be explicitly included (see **variable**,
**output**, **function**, ...). A custom test can be selected with the
**test** keyword.

The behavior of some of the generated tests can be modified with
additional keys as described in the documentation below.


* **test** key: Indicates a custom test file. Custom tests must be
  stored in the assignment directory under `tests/`. 
  
* **variable** key: Check the value of the variable in **filename**
  after running (actually: importing) the file.

  With **check_type**: `True` can also check the type (default:
  `False`).

* **output** key: Run the code as `python3 filename` and match the
  string in the standard output. By default, this is a *regular
  expression*.

  Can be turned into a bare string with **regular_expression**:
  `False`.

  Be aware of how to structure blocks in yml (e.g., `>` for folded,
  `|` for indented blocks, and `|3` for indented with 3 whitspace
  (e.g., when first line is indented compared to following lines).

* **file**: name of a file that should have been submitted;
  the test only checks that the file exists. 
  
  A path relative to the repository root directory can be used.

 **fileregex**: Python regular expression for one or more
  filenames. If the expression matches at least one filename then the
  test passes.
  
  Directory names do *not* count as matches.
  
  The **fileregex** can be a path including directory names relative
  to the repository root directory. However, regular expressions may
  *only be used for the filename part* as directory parts of the path
  are never matched but used literally.

* **imagefilename**: name of a file that should have been submitted;
  the test only checks that the file exists and that it can be loaded
  as an image with `matplotlib.image.imread()`.
  
* **content**: multiline regular expression (like **output**) but
  matches the *content* of **filename**.

* **function:** key: functions are *always tested with parametrized
  fixtures*, i.e., arguments **args**/**kwargs** must *always* be
  present in a list in the yaml generate file.
  
  Entries in **args** and **kwargs** are paired (like `zip(args,
  kwargs)`). 

  Functions are always called with `func(*args, **kwargs)` for each
  parameter set.

  The list of **reference** values must have the same length as the
  **args** and **kwargs** lists, with one reference for each input.

  Only one of **args** or **kwargs** need to be provided; the other is
  generated with empty content if necessary.

##### Test parameters

* **input_values** key: input to be read from standard input. Each
  element of the list is turned into a string and supplied with a
  newline.
  
* **args**: arguments for a **function** test as a list of lists

* **kwargs**: keyword arguments for a **function** test as a list of
  dictionaries
  
* **reference**: reference values to compare the output of a
  **function** test against.  The list of **reference** values must
  have the same length as the **args** and **kwargs** lists, with one
  reference for each input.
  
  If a tested value is a numpy array or a tuple of numpy arrays then
  the reference is converted to a numpy array or tuple of numpy arrays
  for the test with `numpy.testing.assert_allclose()`. Otherwise,
  numbers are tested with `pytest.approx` or with `==`. The
  **absolute_tolerance** and **relative_tolerance** values are used
  for either the numpy or the pytest comparison.

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
  
  If an array comparison with `assert_allclose()` is performed, the
  tolerances behave like [`np.allclose(actual, desired, rtol,
  atol)`](https://numpy.org/doc/stable/reference/generated/numpy.allclose.html)
  where the difference between `actual` and `desired` to `atol +
  rtol * abs(desired)` is compared.

* **check_type**: `True` or `False` (default): also check the type for
  a **variable** test
  
* **regular_expression**: `True` (default) or `False`: select if the
  reference value for **output** is treated as Python regular
  expression (`True`) or matched as a bare string (`False`).

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
hw02/
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
  
