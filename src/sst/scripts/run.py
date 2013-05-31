#!/usr/bin/env python
#
#   Copyright (c) 2011-2012 Canonical Ltd.
#
#   This file is part of: SST (selenium-simple-test)
#   https://launchpad.net/selenium-simple-test
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#


import datetime
import os
import subprocess
import sys
import time
import urllib

import testtools

testtools.try_import('selenium')

import sst
from sst import (
    browsers,
    command,
    runtests,
    tests,
)


def main():
    cmd_opts, args = command.get_opts_run()

    print '--------------------------------------------------------------'
    print 'starting SST...'

    cleaner = command.Cleaner(sys.stdout)

    if cmd_opts.run_tests:
        cmd_opts.dir_name = 'selftests'
        if not tests.check_devserver_port_used(sst.DEVSERVER_PORT):
            run_django(sst.DEVSERVER_PORT)
            cleaner.add('killing django...\n', kill_django, sst.DEVSERVER_PORT)
        else:
            print 'Error: port is in use.'
            print 'can not launch devserver for internal tests.'
            sys.exit(1)

    if cmd_opts.xserver_headless:
        from sst.xvfbdisplay import Xvfb
        print '\nstarting virtual display...'
        display = Xvfb(width=1024, height=768)
        display.start()
        cleaner.add('stopping virtual display...\n', display.stop)

    if not cmd_opts.quiet:
        print ''
        print '  date time: %s' \
            % datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        print '  test directory: %r' % cmd_opts.dir_name
        print '  report format: %r' % cmd_opts.report_format
        print '  browser type: %r' % cmd_opts.browser_type
        print '  shared directory: %r' % cmd_opts.shared_directory
        print '  screenshots on error: %r' % cmd_opts.screenshots_on
        print '  failfast: %r' % cmd_opts.failfast
        print '  debug: %r' % cmd_opts.debug
        print '  concurrency enabled: %r' % cmd_opts.use_concurrency
        print '  headless xserver: %r' % cmd_opts.xserver_headless
        print ''

    with cleaner:
        command.clear_old_results()
        factory = browsers.browser_factories.get(cmd_opts.browser_type)
        failures = runtests.runtests(
            args,
            test_dir=cmd_opts.dir_name,
            collect_only=cmd_opts.collect_only,
            report_format=cmd_opts.report_format,
            browser_factory=factory(cmd_opts.javascript_disabled),
            shared_directory=cmd_opts.shared_directory,
            screenshots_on=cmd_opts.screenshots_on,
            concurrency_num=int(cmd_opts.concurrency),
            failfast=cmd_opts.failfast,
            debug=cmd_opts.debug,
            extended=cmd_opts.extended_tracebacks,
            excludes=cmd_opts.excludes
        )

    return failures


def run_django(port):
    """Start django server for running local self-tests."""
    here = os.path.abspath(os.path.dirname(__file__))
    manage_file = os.path.abspath(
        os.path.join(here, '../../testproject/manage.py'))
    url = 'http://localhost:%s/' % port

    if not os.path.isfile(manage_file):
        print 'Error: can not find the django testproject.'
        print '%r does not exist' % manage_file
        print 'you must run self-tests from the dev branch or package source.'
        sys.exit(1)

    django = testtools.try_import('django')
    if django is None:
        print 'Error: can not find django module.'
        print 'you must have django installed to run the test project.'
        # FIXME: Using sys.exit() makes it hard to test in isolation. Moreover
        # this error path is not covered by a test. Both points may be related
        # ;) -- vila 2013-05-10
        sys.exit(1)
    proc = subprocess.Popen([manage_file, 'runserver', port],
                            stderr=open(os.devnull, 'w'),
                            stdout=open(os.devnull, 'w')
                            )
    print '--------------------------------------------------------------'
    print 'waiting for django to come up...'
    attempts = 30
    for count in xrange(attempts):
        try:
            resp = urllib.urlopen(url)
            if resp.code == 200:
                break
        except IOError:
            time.sleep(0.2)
            if count >= attempts - 1:  # timeout
                print 'Error: can not get response from %r' % url
                raise
    print 'django found. continuing...'
    return proc


def kill_django(port):
    try:
        urllib.urlopen('http://localhost:%s/kill_django' % port)
    except IOError:
        pass


if __name__ == '__main__':
    failures = main()
    if failures:
        sys.exit(1)
