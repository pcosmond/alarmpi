#!/usr/bin/python

import os

processname='fftxalarm.py'
tmp = os.popen("ps -Af").read()
procount = tmp.count(processname)

if procount > 0:
    print (procount, 'processes running of', processname)
#    return (0)
