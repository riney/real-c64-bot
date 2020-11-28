#!/usr/bin/sh

sudo apt-get install xa65 build-essential byacc texi2html flex libreadline-dev libxaw7-dev texinfo libxaw7-dev libgtk2.0-cil-dev libgtkglext1-dev libpulse-dev dos2unix subversion
svn checkout https://svn.code.sf.net/p/vice-emu/code/trunk vice-emu-code
cd vice-emu-code/vice
./autogen.sh
./configure --enable-headlessui --disable-pdf-docs --without-alsa
make
sudo make install