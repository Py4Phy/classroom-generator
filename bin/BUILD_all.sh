#!/bin/bash

BUILD=$1
TOPDIR=/Volumes/ASU/oliver/Documents/Teaching/ASU/CompPhys_PHY494/2021/Classroom/classroom-generator
ASSETS=$TOPDIR/assets
BINDIR=$TOPDIR/bin


function die () {
    echo "ERROR: $1"
    exit 1;
}

$BINDIR/generate_tests.py || die "generator failed"

test -n "$BUILD" || die "usage: $0 BUILD_DIR"
test -d "$BUILD" || die "no dir $BUILD"

echo "## Finalizing repo"

cp -v README.md assignment*.md assignment*.pdf $BUILD
cp -v *.py $BUILD
# Should not need to copy tests: use test_assets: ["conftest.py", ...] at top.
#test -d tests && rsync -avP --exclude="__pycache__" --exclude="*~" tests $BUILD
mkdir -p $BUILD/.github/{workflows,classroom}
cp -v $ASSETS/workflows/classroom.yml $BUILD/.github/workflows
mv $BUILD/autograding.json $BUILD/.github/classroom/
cp -v $ASSETS/students.gitignore $BUILD/.gitignore

(cd $BUILD && test -d .git ||  { git init && git add -A . && git commit -m "initialized assignment"; } && { git add -A . && git commit -m "updated assignment"; })
