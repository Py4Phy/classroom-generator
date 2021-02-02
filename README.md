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
- custom test files


## Usage

Primitive at the moment... will create the new HW in a directory
`BUILD/HWxx`, which needs to be manually copied as necessary.



### Assignment
Create the assignment.md.

Make sure to include the points banner.

### Starter code

Manually copy any starter code.

### Classroom workflow
1. Manually copy a working `.github/workflows/classroom.yml`


### Generating tests

Tests are generated in the BUILD directory, typically "BUILD/HWxx"; we
will refer to it as `$BUILD`.

1. cd hw working directory with `generate.yml` 
2. run `generate_tests.py`, which creates `$BUILD`


### Tests infrastructure

All necessary files are copied into the `$BUILD` directory. 

### Final assembly

- copy assignment.md to `$BUILD` and symlink as README.md
- copy assignment assets to `$BUILD`
- `mkdir $BUILD/.github/{workflows,classroom}`
- copy classroom.json `cp $ASSETS/workflows/classroom.yml $BUILD/.github/workflows` (does not change)
- copy autograding.json `cp autograding.json $BUILD/.github/classroom` (is specific for this assignment)
- create .gitignore
- create a  *template* repository for the HWxx,  `cd $BUILD && git init && git add . && git commit`, push to the repo




## Solutions

Keep solutions in a `solution` directory here for reference. They are
not used anywhere. The `generate.yml` file needs to either contain the
correct reference values or the custom tests need to contain the code
to check for correctness.



## TODO
- add commandline processing to script
- put all files in the template (assignment.md, classroom.yml) and copy
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