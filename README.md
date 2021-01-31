# Homeworks Test Templates

Homework tests are generated from templates and a `solution.yml` file that contains the individual tests with points. The `generate_tests.py` script then creates

- the appropriate tests themselves
- the `autograding.json` configuration for the `.github/workflows/classroom/autograding.json`


## Usage

Primitive at the moment...

### Assignment
Create the assignment.md and symlink to README.md.

Make sure to include the points banner.

### Classroom workflow
1. Manually copy a working `.github/workflows/classroom.yml`


### Tests infrastructure
1. In hw working dir, `mkdir tests` 
2. Manually copy `tst.py` to `tests` directory.


### Generating tests

1. cd hw working directory tests dir
2. symlink `solution.yml` to the hw tests working directory
3. run `generate_tests.py` in the hw tests working dir 
4. mv new autograding.json to `.github/classroom`
5. add & commit all new files


## Solutions
Keep solutions in a `solution` directory here for reference.


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
├── assignments
│   ├── ...
│   └── hw03
│       └── solution.yml
└── bin
    ├── ...
    └── generate_tests.py
```