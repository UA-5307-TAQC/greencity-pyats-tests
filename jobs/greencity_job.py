"""This script serves as the entry point
for executing the test suite using pyATS."""
import sys
import os
import multiprocessing

import project_root
from pyats.easypy.tasks import run

multiprocessing.set_start_method("spawn", force=True)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ['PYTHONPATH'] = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

def main(runtime):
    """Main function to execute the test suite."""

    testbed = runtime.testbed

    if testbed is None:
        raise ValueError("Testbed is not provided! Use --testbed-file")

    run("tests/common_setup.py", testbed=testbed, taskid="common_setup")
    run("tests/test_auth.py", testbed=testbed, taskid="test_auth")
    run("tests/test_user_profile.py", testbed=testbed, taskid="test_user_profile")
    run("tests/test_habits.py", testbed=testbed, taskid="test_habits")
    run("tests/test_security.py", testbed=testbed, taskid="test_security")
    run("tests/test_rbac.py", testbed=testbed, taskid="test_rbac")
    run("tests/test_negative_api.py", testbed=testbed, taskid="test_negative_api")
    run("tests/test_performance.py", testbed=testbed, taskid="test_performance")
