from ftplib import FTP
from telnetlib import Telnet

def upload_program(host=None, dir=None, program, name=None):
    # TODO: get defaults from Config
    with FTP(host) as ftp:
        ftp.login()
        if dir:
            ftp.cwd(dir)

        with open(program, 'rb') as prg:
            ftp.storbinary(f"STOR #{name}", prg)
        
        ftp.quit()

def run_program(host=None):
    # TODO: get defaults from Config
    with Telnet(host, 23) as telnet:
        telnet.write(chr(27) + b"[A")
