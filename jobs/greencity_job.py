from pathlib import Path
import sys
from pyats.easypy import run
from pyats.topology import loader
from pyats.results import Passed

project_root_path = Path(__file__).parent.parent.absolute()
project_root = str(project_root_path)

if project_root not in sys.path:
    sys.path.append(project_root)

def main(runtime):
    tb_path = project_root_path / "config" / "testbed.yaml"
    testbed = loader.load(str(tb_path))

    task = run(
        testscript="tests/test_reachability.py",
        testbed=testbed,
        taskid="Test_Reachability"
    )

    if task != Passed:
        return

    run(
        testscript="tests/test_user_profile.py",
        testbed=testbed,
        taskid="Test_Authentication"
    )

    run(
        testscript="tests/test_habits.py",
        testbed=testbed,
        taskid="Test_Habits"
    )

    run(
        testscript="tests/test_negative_api.py",
        testbed=testbed,
        taskid="Negative_API_Tests"
    )

    run(
        testscript="tests/test_security.py",
        testbed=testbed,
        taskid="Security_Tests"
    )

    run(
        testscript="tests/test_rbac.py",
        testbed=testbed,
        taskid="Role_Based_Access_Control_Tests"
    )

    run(
        testscript="tests/test_ddt.py",
        testbed=testbed,
        taskid="Data_Driven_Testing "
    )

    run(
        testscript="tests/test_performance.py",
        testbed=testbed,
        taskid="Test_Performance "
    )
