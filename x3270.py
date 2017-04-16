# This work is licensed under a Creative Commons Attribution-ShareAlike 4.0 International License.
# https://creativecommons.org/licenses/by-sa/4.0/
# Created by Marcin Kocur <marcin2006 AT gmail DOT com>, 2017

#!/usr/bin/python

import subprocess
import sys
from time import sleep

class X3270:
    pass
    
    def __init__(self, pid, win_title):
        self.pid = pid
        self.win_title = win_title
    
    def get_output(self):
        output = subprocess.Popen(["x3270if", "-p", self.pid, "ascii"], stdout=subprocess.PIPE).communicate()[0]
        return output
        
    def get_position(self):
        return subprocess.Popen(["x3270if", "-p", self.pid, 'query("cursor")'], stdout=subprocess.PIPE).communicate()[0].strip()
        
    def set_position(self, position):
        position = position.replace(' ', ',') # so you can type position with coma or with space
        subprocess.call(["x3270if", "-p", self.pid, 'MoveCursor(' + position + ')'])
    
    def confirm(self):
        subprocess.call(["x3270if", "-p", self.pid, "enter"])
        
    def PF(self, number):
        subprocess.call(["x3270if", "-p", self.pid, "PF(" + str(number) + ")"])
        
    def type_in(self, string, position= 'None'):
        x3270_position = X3270.get_position(self)
        position = position.replace(',', ' ') # so you can type position with coma or with space
        def x3270_write(self, string):
            subprocess.call(["x3270if", "-p", self.pid, 'string(' + string + ')'])

        if position == 'None':
            x3270_write(self, string)
            print("position is empty")
        elif x3270_position == position:
            print("position is equal")
            x3270_write(self, string)
            return True
        else:
            if __name__ == "__main__":
                print("Position is different. I will exit so nothing gets broken.")
                exit()
            return False

    def wait_for(self, string, timeout=50):
        output = X3270.get_output(self)
        counter = 0
        if timeout == 'unlimited':
            timeout = float("inf")
        while string not in output:
            sleep(0.5) #first sleep half a second for 10 seconds
            counter += 1
            output = X3270.get_output(self)
            print(counter)
            if counter >= timeout:
                subprocess.call(['notify-send', '-u', 'normal', '-t', '30000', '-i', sys.path[0]+'/process-stop.png', self.win_title, 'The window does not work properly, script terminated.'])
                exit()
            if counter >= 30 and counter < timeout:
                print("now sleeping 10 seconds")
                sleep(10)
            if counter >= 20 and counter < 30:
                print("now sleeping 5 seconds")
                sleep(5)
            if counter >= 10 and counter < 20: # then sleep a second for 10 seconds
                print("now sleeping half a second more")
                sleep(0.5)
        else: return True
