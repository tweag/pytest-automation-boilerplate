#!/bin/sh

# User should be running this script as `source install.sh`, not `sh install.sh`
PLATFORM_TYPE=$(command uname)

# Run Steps that is not dependent on python virtual environment
python ./install.py global

RETCODE=$?
if [ $RETCODE = 0 ]; then
    # Activate Virtual Environment at the end of install script.

    if [ "$PLATFORM_TYPE" = "Darwin" ]; then
        . $HOME/.bp-venv/bin/activate
    elif [ "$PLATFORM_TYPE" = "Linux" ]; then
        . $HOME/.bp-venv/bin/activate
    else
        . $HOME\\.bp-venv\\Scripts\\activate
    fi
else
    # Don't Do anything. install.py should take care of it.
    true
fi

echo "Activated Virtual Environment .bp-venv..."
echo "\n"

# Activate Virtual Environment and then run remaining installation steps that's dependent on venv & dependencies.
python ./install.py venv

RETCODE=$?
if [ $RETCODE = 0 ]; then

    if [ "$PLATFORM_TYPE" = "Windows" ]; then
        echo -e "Yet another Important Note: Please activate virtual environment using command \". $HOME\\.bp-venv\\Scripts\\activate\" while running test cases from new shell. Need not activate now, since it is already activated."
    else
        echo -e "Yet another Important Note: Please activate virtual environment using command \". $HOME/.bp-venv/bin/activate\" while running test cases from new shell. Need not activate now, since it is already activated."
    fi
else
    # Don't Do anything. install.py should take care of it.
    true
fi
