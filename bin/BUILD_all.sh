#!/bin/bash

TOPDIR=$(cd "$(dirname $0)/.." && pwd)
ASSETS="${TOPDIR}/assets"
BINDIR="${TOPDIR}/bin"

E_OPTERROR=85

USAGE="$0 [-B BUILDIR] SRCDIR

Run the classroom-generator in SRCDIR and copy
all files to a repository under BUILDIR.

The default for BUILDIR is SRCDIR/BUILD.

-B DIR         build directory, e.g., /tmp/BUILD/
"

function die () {
    echo "ERROR: $1"
    exit 1;
}

BUILD=""
while getopts "B:h" Option
do
    case $Option in
	B) BUILD="$OPTARG";;
	h) echo "$USAGE"; exit 0;;
	*) die "unknown option" $E_OPTERROR;;
    esac
done
shift $(($OPTIND - 1))

SRCDIR="$1"
: "${BUILD:=${SRCDIR}/BUILD}"

echo "## $0 ($(date))"
echo ".. SRCDIR = $SRCDIR"
echo ".. BUILD = $BUILD"


# generator script decides on the name of the directory so we grep it
# from the output
echo ">> generate_tests.py --build-dir ${BUILD} ${SRCDIR}"
dest_dir=$("${BINDIR}/generate_tests.py" --build-dir "${BUILD}" "${SRCDIR}" | awk '/^BUILD_DIR:/ {printf $2}')
test -n "${dest_dir}"  || die "generator script failed"
test -d "${dest_dir}" || die "generated files are missing: no directory ${dest_dir}" 2

echo "## Finalizing repo in ${dest_dir}"

cp -v README.md assignment*.md assignment*.pdf tex/*.pdf "${dest_dir}"
cp -v *.csv *.txt "${dest_dir}"
cp -v *.py *.ipynb "${dest_dir}"
# Should not need to copy tests: use test_assets: ["conftest.py", ...] at top.
#test -d tests && rsync -avP --exclude="__pycache__" --exclude="*~" tests "${dest_dir}"
mkdir -p "${dest_dir}/.github/workflows" "${dest_dir}/.github/workflows/classroom"
cp -v "${ASSETS}/workflows/classroom.yml" "${dest_dir}/.github/workflows"
mv "${dest_dir}/autograding.json" "${dest_dir}/.github/classroom/"
cp -v "${ASSETS}/students.gitignore" "${dest_dir}/.gitignore"

(cd "${dest_dir}" && test -d .git ||  { git init && git add -A . && git commit -m "initialized assignment"; } && { git add -A . && git commit -m "updated assignment"; })

echo "## completed ${dest_dir}"
