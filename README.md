# Homeworks Test Templates

Homework tests are generated from templates and a `generate.yml` file
that contains the individual tests with points. The
`generate_tests.py` script then creates

- the appropriate tests themselves
- the `autograding.json` configuration for the `.github/workflows/classroom/autograding.json`

The `solutions.yml` file indicates problems with their individual
tests. For each problem, a subdirectory is made under tests. Each test
gets its own test file, point value, and entry in `autograding.yml`.

At the moment the following is supported:
- template tests for checking fixed variables
- template tests for running a script with `input()` from stdin that sets variables
- template test for comparing output against regular expression
- custom test files


## Usage

Primitive at the moment... will create the new HW in a directory
`BUILD/HWxx`, which needs to be manually copied as necessary.

### Assignment

Create the assignment.md.

Make sure to include the points banner.

### Starter code

Create any starter code.


### Generating tests

Tests are generated in the BUILD directory, typically "BUILD/HWxx"; we
will refer to it as `$BUILD`.

1. cd hw working directory with `generate.yml` 
2. run `generate_tests.py`, which creates `$BUILD`

See below for notes on `generate.yml`


### Tests infrastructure

All necessary files are copied into the `$BUILD` directory. 

### Final assembly

Can use the

    bin/BUILD_all BUILD/<name>`

script, which does the following:

- copy assignment.md to `$BUILD` and symlink as README.md
- copy assignment assets to `$BUILD`
- `mkdir $BUILD/.github/{workflows,classroom}`
- copy classroom.json `cp $ASSETS/workflows/classroom.yml $BUILD/.github/workflows` (does not change)
- copy autograding.json `cp autograding.json $BUILD/.github/classroom` (is specific for this assignment)
- create .gitignore
- create a  *template* repository for the HWxx,  `cd $BUILD && git init && git add . && git commit`, push to the repo


## generate.yml

Look at existing ones for examples. Example with common usage:

```yaml
problemset:
  name: HW example
  test_assets: ["conftest.py"]
  problems:
  - problem: 1
    title: Copy, rename, delete
    filename: "PHY494/"
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
``` 
          
          


## Solutions

Keep solutions in a `Solution` directory here for reference. They are
not used anywhere. The `generate.yml` file needs to either contain the
correct reference values or the custom tests need to contain the code
to check for correctness.



## TODO
- add commandline processing to script
- put all files in the template (assignment.md, classroom.yml) and copy -- see `BUILD_all.sh`
- documentation


## Layout

fixed directory structure

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
├── Assignments
│   ├── ...
│   └── hw03
│       └── generate.yml
└── bin
    ├── ...
    └── generate_tests.py
```