#!/bin/bash

# Stop on errors.
set -e

# Fix root directory.
cd "$(dirname $(readlink -f "${BASH_SOURCE[0]}"))/.."

# Import constants.
. scripts/constants.sh


main() {
    install-dependencies
    create-virtual-environment
    echo "done"
}


install-dependencies() {
    echo "installing dependencies..."
    sudo apt-get install -y \
        build-essential \
        coreutils \
        findutils \
        git \
        python3
}


create-virtual-environment() {
    echo "creating virtual environment..."
    if [ -d "$VENV" ]
    then
        echo "virtual environment $VENV already exists"
        return
    fi

    # Create virtual environment with a user-friendly prompt.
    python3 -m venv "$VENV" --prompt="$NAME"

    # Install requirements.
    "$VENV/bin/pip" install -U pip build pytest
    "$VENV/bin/pip" install -r requirements.txt

    # Make package importable from anywhere.
    find . -name site-packages -exec bash -c 'echo "$(realpath --relative-to="{}" "$PWD")" > "{}/self.pth"' \;
}


main "$@"