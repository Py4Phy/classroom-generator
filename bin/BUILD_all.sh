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

CONFIG="$1"
SRCDIR=$(dirname "${CONFIG}")
: "${BUILD:=${SRCDIR}/BUILD}"

echo "## $0 ($(date))"
echo ".. CONFIG = $CONFIG"
echo ".. SRCDIR = $SRCDIR"
echo ".. BUILD = $BUILD"

test -n "${CONFIG}" || die "missing YML config file"
test -d "${SRCDIR}" || die "no SRCDIR ${SRCDIR} for ${CONFIG}" 2

# generator script decides on the name of the directory so we grep it
# from the output
echo ">> generate_tests.py --build-dir ${BUILD} ${CONFIG}"
logfile=$(mktemp -t generate_test_output)
"${BINDIR}/generate_tests.py" --build-dir "${BUILD}" "${CONFIG}" 2>&1 | tee $logfile || die "generate_tests failed" $?
# WARNING: next line breaks if BUILD_DIR contains spaces (due to white-space splitting and $2)...
dest_dir=$(awk '/^BUILD_DIR:/ {printf $2}' $logfile)
rm $logfile

test -n "${dest_dir}"  || die "generator script failed"
test -d "${dest_dir}" || die "generated files are missing: no directory ${dest_dir}" 2

echo "## Finalizing repo in ${dest_dir}"

## all assets are listed in generate.yml and are copied with generate_tests.py
## Use assets: ["README.md", ...] at top level and assets: ["data.csv", "startercode.py"] at the problem level

mkdir -p "${dest_dir}/.github/workflows" "${dest_dir}/.github/classroom"
cp -v "${ASSETS}/workflows/classroom.yml" "${dest_dir}/.github/workflows"
mv "${dest_dir}/autograding.json" "${dest_dir}/.github/classroom/"
cp -v "${ASSETS}/students.gitignore" "${dest_dir}/.gitignore"

(cd "${dest_dir}" && test -d .git ||  { git init && git add -A . && git commit -m "initialized assignment"; } && { git add -A . && git commit -m "updated assignment"; })

echo "## completed ${dest_dir}"
