#!/bin/sh
echo "Installing default venv..."
python3 -m venv venv/default
echo "Installing python 3.5 venv..."
python3.5 -m venv venv/py35
echo "Installing python 3.6 venv..."
python3.6 -m venv venv/py36
echo "Installing python 3.7 venv..."
python3.7 -m venv venv/py37
echo "Installing python 3.8 venv..."
python3.8 -m venv venv/py38
