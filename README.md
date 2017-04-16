x3270.py can be used as python library for interacting in script mode with x3270 mainframe terminal emulator.

Example usage:

1. Create a login script which you run with following arguments: script.py LOGIN PASSWORD


#!/usr/bin/python

from x3270 import *
import subprocess

class MySystem:
    window_title = '''Some window title'''
    
    def __init__(self):
        self.login = sys.argv[1]
        self.password = sys.argv[2]
        if len(self.login) < 7:
            print("Your login is wrong")
            exit()
        if len(self.password) < 7:
            print("Your password is wrong")
            exit()

@classmethod
    def login_procedure(cls):
        system = subprocess.Popen(['x3270', '-socket', '-model', '3279-3', '-efont', '3270-12', '-charset', 'us-intl', '-title', cls.window_title, '-proxy', 'SOCKS5:XXX.XXX.XXX:1080', 'mainframe_server:23'])
        pid = str(system.pid)
        with open('pid', 'w') as open_file:
            open_file.write(cls.window_title + "PID:" + pid )
        print('pid is',pid)
        system = X3270(pid, cls.window_title)
        system.wait_for('''

*************** 
INITIAL PROMPT
********************

''')
        system.type_in(sys.argv[1], '10 19') # enters login only if on position 10, 19
        system.set_position('12 19')
        system.type_in(sys.argv[2], '14 19') # enters password only if on position 14, 19
        system.confirm()
        system.wait_for(' MAIN MENU ')
        system.type_in('1') #types-in 1 without checking position
        system.confirm()
        system.wait_for('SECOND MENU')

if __name__ == "__main__":
    
    system_login = System()
    system_login.login_procedure()



2. Then you can create second script which takes over session created by login script:

#!/usr/bin/python
def pid():
    with open(dirname(sys.argv[0])+'/pid', 'r') as open_file:
        for line in open_file:
            if 'Some window title' in line:
                pid = line.split('PID:')[1]
                return str(pid)


3. And does something useful:

def system_can_i_delete_job():
    output = get_output(pid)

def system_remove_job():
    PF(5, pid)

if system_can_i_delete_job():
            system_remove_job()
        else:
            subprocess.Popen(["paplay", dirname(sys.argv[0])+"/alert.ogg"])