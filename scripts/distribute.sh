#!/bin/bash

# Stop on errors.
set -e

# Fix root directory.
cd "$(dirname $(readlink -f "${BASH_SOURCE[0]}"))/.."

# Import constants.
. scripts/constants.sh


main() {
    build-package
    install-package
    clean-package
    echo "done"
}


build-package() {
    echo "building package..."
    "$VENV/bin/python" -m build --wheel
}


install-package() {
    echo "installing package..."
    pip install dist/*.whl
}


clean-package() {
    echo "cleaning package..."
    rm -rf build dist *.egg-info
}


main "$@"