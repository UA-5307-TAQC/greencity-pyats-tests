# greencity-pyats-tests

## Project Structure
```
greencity-pyats-tests/
├── jobs/
│   └── greencity_job.py        # Job file to aggregate and run tests
├── tests/
│   ├── test_auth.py            # Authentication logic
│   ├── test_habits.py          # Functional CRUD tests
│   └── test_security.py        # Negative and RBAC tests
├── utils/
│   ├── api_client.py           # Requests wrapper with logging
│   └── schema_validator.py     # JSON Schema definitions
├── config/
│   ├── testbed.yaml            # Environment & Device config
│   └── test_data.yaml          # Parameters for DDT
└── requirements.txt            # pyATS, requests, jsonschema
```

## Deliverables
Codebase: Clean, PEP 8 compliant Python code.

Logs: Detailed pyATS logs showing step-by-step execution.

Report: An HTML summary report (generated via pyats run job --html-logs).

README: Clear instructions on how to set up the environment and run the tests.

## Run

```cmd
pyats run job jobs/job.py
```
