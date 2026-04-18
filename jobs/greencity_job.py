from pyats.easypy import run
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


def main():
    run("tests/test_environment.py")
    run("tests/test_auth.py")
    run("tests/test_security.py")
    run("tests/test_habits.py")
    run("tests/test_profile.py")
    run("tests/test_habits_crud.py")
    run("tests/test_negative.py")
    run("tests/test_auth_integrity.py")
    run("tests/test_rbac.py")
    run("tests/test_ddt.py")
    run("tests/test_stability.py")
