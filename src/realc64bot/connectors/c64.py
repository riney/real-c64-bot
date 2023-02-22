import os
import subprocess
from realc64bot.config import Config

def tokenize(text_to_tokenize, filename, path=None):
    config = Config().values()

    if path == None:
        path = config['locations']['programs']

    command = config['commands']['tokenize']
    
    subprocess.run(["petcat", "-w2", "-o", path / filename],
                   input=bytes(text_to_tokenize, 'utf-8'))
    