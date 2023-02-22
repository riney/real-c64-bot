import os
import pytest

def test_vicetools_exists():
    retval = os.system('which petcat')
    assert os.waitstatus_to_exitcode(retval) == 0
