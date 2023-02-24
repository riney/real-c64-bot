import os
import pytest
from realc64bot.connectors.vicetools import tokenize

def test_vicetools_exists():
    retval = os.system('which petcat')
    assert os.waitstatus_to_exitcode(retval) == 0

def test_tokenize(tmp_path):
    # setup temp dirs
    temp_programs_dir = tmp_path / "programs"
    os.mkdir(temp_programs_dir)

    # tokenize
    test_input = '10 PRINT "HELLO WORLD"'
    tokenize(test_input, 'out.prg', temp_programs_dir)

    # assert stuff
    size = os.path.getsize(temp_programs_dir / 'out.prg')
    assert size == 28 # yes, this is how big it should be
