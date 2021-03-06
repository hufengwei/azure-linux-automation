#!/usr/bin/python

from azuremodules import *


import argparse
import sys
import time
import re
        #for error checking
parser = argparse.ArgumentParser()

parser.add_argument('-e', '--expected', help='specify expected hostname', required=True)

args = parser.parse_args()
                #if no value specified then stop
expectedHostname = args.expected

def RunTest(expectedHost):
    UpdateState("TestRunning")
    if CheckHostName(expectedHost) and CheckFQDN(expectedHost):
        ResultLog.info('PASS')
        UpdateState("TestCompleted")
    else:
        ResultLog.error('FAIL')
        UpdateState("TestCompleted")

def CheckHostName(expectedHost):
    RunLog.info("Checking hostname...")
    output = Run("hostname")
    if expectedHost.lower() in output.lower():
        RunLog.info('Hostname is set successfully to {0}'.format(expectedHost))
        return True
    else:
        RunLog.error('Hostname change failed. Current hostname : {0} Expected hostname : {1}'.format(output, expectedHost))
        return False

def CheckFQDN(expectedHost):
    RunLog.info("Checking fqdn...")
    [current_distro, distro_version] = DetectDistro()
    nslookupCmd = "nslookup {0}".format(expectedHost)
    if current_distro == 'coreos':
        nslookupCmd = "python nslookup.py -n {0}".format(expectedHost)
    output = Run(nslookupCmd)
    if re.search("server can't find", output) is None:
        RunLog.info('nslookup successfully for: {0}'.format(expectedHost))
        return True
    else:
        RunLog.error("nslookup failed for: {0}, {1}".format(expectedHost, output))
        return False


RunTest(expectedHostname)
