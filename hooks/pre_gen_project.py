import re
import sys


PROJECT_NAME_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'
project_name = '{{cookiecutter.project_name}}'

if not re.match(PROJECT_NAME_REGEX, project_name):
    print('ERROR: %s is not a valid Go Project name!' % project_name)
    # exits with status 1 to indicate failure
    sys.exit(1)