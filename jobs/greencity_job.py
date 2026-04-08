import os
import sys
from pyats.easypy import run

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

current_pythonpath = os.environ.get('PYTHONPATH', '')
os.environ['PYTHONPATH'] = f"{project_root}:{current_pythonpath}"

def main(runtime):
    test_path = os.path.join(os.path.dirname(__file__), '..', 'tests')

    run(testscript=os.path.join(test_path, 'test_auth.py'), runtime=runtime)
    run(testscript=os.path.join(test_path, 'test_profile.py'), runtime=runtime)
    run(testscript=os.path.join(test_path, 'test_crud.py'), runtime=runtime)
    run(testscript=os.path.join(test_path, 'test_negative.py'), runtime=runtime)
    run(testscript=os.path.join(test_path, 'test_security.py'), runtime=runtime)
    run(testscript=os.path.join(test_path, 'test_rbac.py'), runtime=runtime)
    run(testscript=os.path.join(test_path, 'test_data_driven.py'), runtime=runtime)
    run(testscript=os.path.join(test_path, 'test_performance.py'), runtime=runtime)