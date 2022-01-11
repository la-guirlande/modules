# Modules source code

This project contains all implementations of different modules used in the Guirlande Hub.

The [Module Client library](https://github.com/la-guirlande/module-client) is used to communicate with the backend.

# Install Python
wget -qO - https://raw.githubusercontent.com/tvdsluijs/sh-python-installer/main/python.sh | sudo bash -s 3.10.0

# If error when installing RPi.GPIO
env CFLAGS="-fcommon" pip install rpi.gpio