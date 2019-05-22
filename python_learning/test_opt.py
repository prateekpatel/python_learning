from optparse import OptionParser
import DevopsLogging
import json
import psql
import subprocess
import xml.etree.ElementTree as ET
import os
import re
import requests
from requests.auth import HTTPBasicAuth

def execute_shell_command(cmd):
    """
    To execute confluence command and return output.
    :param cmd: Command to be executed
    :return: output(Html content of the given confluence page)
    """
    #logger.debug("Confluence Command: \'%s\' " % (cmd))
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output




def branch_validation(branch):
    pattern = "^(master|hotfix|patch|.*_ib|.*_rb)$"
    return bool(re.match(pattern, branch))




def main():
    global logging
    global connection
    logging = DevopsLogging.get_logger('DEBUG')
    connection = psql.Postgresql()

    parser = OptionParser(usage="usage: %prog [OPTIONS]")
    parser.add_option("-p", "--project", type="string",
                      help="project name for CI",
                      dest="project")
    parser.add_option("-b", "--branch", type="string",
                      help="branch name for CI",
                      dest="branch")

    (options, args) = parser.parse_args()

    if options.project and options.branch:
        tag_validation(options.project, options.branch)




if __name__ == '__main__':
    main()
