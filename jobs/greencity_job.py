"""run all tests"""
import os
import sys
from pyats.easypy import run

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

os.environ['PYTHONPATH'] = f"{project_root}:{os.environ.get('PYTHONPATH', '')}"

def main(runtime):
    """run all tests"""
    test_path = os.path.join(project_root, 'tests')

    run(testscript=os.path.join(test_path, 'test_greencity_profile.py'),runtime=runtime,)
