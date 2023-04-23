import pytest
from realc64bot.workers.queue_worker import WorkQueue

def test_connect():
    queue = WorkQueue()

    assert queue.connection is not None

def test_enqueue():
    assert True    
