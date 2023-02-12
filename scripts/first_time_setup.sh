#!/bin/bash

# Sets up dev environment, at least on Ubuntu.

#sudo apt update
#sudo apt -y install build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
#libsqlite3-dev curl libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
#libffi-dev liblzma-dev libpq-dev

#curl https://pyenv.run | bash

# echo '' >> ~/.bash_profile
# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
# echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
# echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
# echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile

# echo '' >> ~/.bashrc
# echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
# echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
# echo 'eval "$(pyenv init -)"' >> ~/.bashrc
# echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# source ~/.bashrc

pyenv install 3.11
pyenv virtualenv-delete venv
pyenv virtualenv 3.11 venv
source ${PYENV_ROOT}/versions/venv/bin/activate

pip install -r requirements.txt
