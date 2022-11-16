#!/bin/bash

# Sets up dev environment, at least on Ubuntu.
sudo apt update
sudo apt install -y build-essential libpq-dev python3 python3-dev python3-pip python3-venv 
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
