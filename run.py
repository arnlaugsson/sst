#!/usr/bin/env python


import optparse
import os
import subprocess
import sys
import time
import urllib

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/src'))
import funcrunner



usage = """Usage: %prog [testname] 

- Calling %prog without any arguments runs all tests in 
the local 'test' directory.

- Calling %prog with testname(s) as arguments will just run 
those tests. The testnames should not include the '.py' at
the end of the filename.

- You may optionally create a data file for data-driven 
testing.  Create a '^' delimited txt data file with the same 
name as the test, plus the '.csv' extension.  This will 
run a test using each row in the data file (1st row of data
file is variable name mapping)
"""



def main():
    (cmd_opts, args) = get_opts()
    
    if cmd_opts.launch_server:
        run_django()
    
    print '----------------------------------------------------------------------'

    funcrunner.runtests(args, test_dir=cmd_opts.dir_name, run_report=cmd_opts.run_report)

    print '----------------------------------------------------------------------'

    if cmd_opts.launch_server:
        kill_django()
        


def run_django():
    subprocess.Popen(['./src/testproject/manage.py', 'runserver'], 
        stderr=open(os.devnull, 'w'), 
        stdout=open(os.devnull, 'w')
        )    
    
    print '----------------------------------------------------------------------'
    print 'Waiting for django to come up...'
    while True:
        try:
            resp = urllib.urlopen('http://localhost:8000/')
            if resp.code == 200:
                break
        except IOError:
            time.sleep(0.2)
    print 'django found. Continuing...'



def kill_django():
    print '\nKilling django...\n'
    os.system("kill $(ps aux | grep 'manage.py' | awk '{print $2}')")


        
def get_opts():
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-d', dest='dir_name', 
                      default='tests', 
                      help='directory of test case files')
    parser.add_option('-r', dest='run_report', 
                      default=False, action='store_true', 
                      help='generate html report instead of console output')
    parser.add_option('-s', dest='launch_server', 
                      default=False, action='store_true', 
                      help='launch django server for local SST framework tests')
    (cmd_opts, args) = parser.parse_args()
    return (cmd_opts, args)
    


if __name__ == '__main__':
    main()

