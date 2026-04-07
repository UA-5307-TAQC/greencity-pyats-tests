"""
pyATS Job — GreenCity EcoNews Creation Tests
---------------------------------------------
Runs all 10 test cases from create_eco_news_testscript.py.

Usage
-----
    pyats run job tests/eco_news/create_eco_news_job.py --testbed testbed.yaml
"""

import os

from pyats.easypy import run

TESTSCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "create_eco_news_testscript.py",
)


def main(runtime):
    """Entry point invoked by the pyATS runtime."""
    run(
        testscript=TESTSCRIPT,
        runtime=runtime,
        taskid="GreenCity_Create_EcoNews",
    )
