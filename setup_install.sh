#!/bin/sh

PLATFORM_TYPE=$(command uname)

# Run Steps that is not dependent on python virtual environment
python ./setup_install.py global

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
    true
fi

echo "Activated Virtual Environment .bp-venv..."
echo "\n"

# Activate Virtual Environment and then run remaining setup steps that's dependent on venv & dependencies.
python ./setup_install.py venv

RETCODE=$?
if [ $RETCODE = 0 ]; then

    if [ "$PLATFORM_TYPE" = "Windows" ]; then
        echo -e "Yet another Important Note: Please activate virtual environment using command \". $HOME\\.bp-venv\\Scripts\\activate\" while running test cases from new shell. Need not activate now, since it is already activated."
    else
        echo -e "Yet another Important Note: Please activate virtual environment using command \". $HOME/.bp-venv/bin/activate\" while running test cases from new shell. Need not activate now, since it is already activated."
    fi
else
    true
fi
