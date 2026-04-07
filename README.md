# greencity-pyats-tests

pyATS black-box test automation framework for the GreenCity external REST API.

---

## Overview

This framework tests the GreenCity REST API using **black-box principles**:

- No access to source code, database, or backend logic
- All interactions are via HTTP only
- Tests are independent and clean up after themselves
- Unique titles prevent conflicts on the shared environment

---

## System Under Test

| Resource    | URL |
|-------------|-----|
| Web App     | https://www.greencity.cx.ua/#/greenCity |
| User API    | https://greencity-user.greencity.cx.ua |
| Main API    | https://greencity.greencity.cx.ua |

---

## Project Structure

```
greencity-pyats-tests/
├── requirements.txt                          # Python dependencies
├── testbed.yaml                              # pyATS testbed (API URLs + credentials)
├── utils/
│   ├── api_client.py                         # GreenCity HTTP client wrapper
│   └── auth_helper.py                        # JWT auth constants / helpers
└── tests/
    └── eco_news/
        ├── create_eco_news_testscript.py     # 10 pyATS test cases
        └── create_eco_news_job.py            # pyATS job runner
```

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure test credentials

Edit `testbed.yaml` and set a valid dedicated test account:

```yaml
custom:
  test_credentials:
    email: "your.test.account@example.com"
    password: "YourTestPassword"
```

---

## Running the Tests

```bash
# Recommended — run via job file (produces full HTML/XML report)
pyats run job tests/eco_news/create_eco_news_job.py --testbed testbed.yaml

# Alternative — run testscript directly
pyats run script tests/eco_news/create_eco_news_testscript.py --testbed testbed.yaml
```

---

## Test Cases

| ID    | Title                                           | Expected Result     |
|-------|-------------------------------------------------|---------------------|
| TC-01 | Create EcoNews with all valid required fields   | 201 Created         |
| TC-02 | Create EcoNews without an auth token            | 401 Unauthorized    |
| TC-03 | Create EcoNews with an invalid / tampered token | 401 or 403          |
| TC-04 | Create EcoNews — missing required `title`       | 400 Bad Request     |
| TC-05 | Create EcoNews — missing required `text`        | 400 Bad Request     |
| TC-06 | Create EcoNews — `title` exceeds max length     | 400 Bad Request     |
| TC-07 | Create EcoNews — empty `tags` list              | 400 Bad Request     |
| TC-08 | Create EcoNews — invalid `tags` value           | 400 Bad Request     |
| TC-09 | Validate response schema on successful creation | 201 + schema check  |
| TC-10 | Create EcoNews and verify it appears in GET list| 201 + 200 in list   |

---

## Design Principles

- **Black-box only** — tests interact exclusively through the REST API
- **Independence** — each test case is self-contained and does not depend on others
- **Unique data** — UUID suffixes in titles prevent conflicts with concurrent users
- **Cleanup** — `CommonCleanup` deletes every article created during the run
- **Graceful degradation** — TC-10 falls back to a direct `GET /econews/{id}` if the
  article is not on the first list page (shared environment may have many articles)

---

## EcoNews API Reference

| Method | Endpoint        | Description                  | Auth     |
|--------|-----------------|------------------------------|----------|
| POST   | `/econews`      | Create a new EcoNews article | Required |
| GET    | `/econews`      | List EcoNews (paginated)     | No       |
| GET    | `/econews/{id}` | Get EcoNews by ID            | No       |
| DELETE | `/econews/{id}` | Delete EcoNews by ID         | Required |

### Create request format

`POST /econews` expects `multipart/form-data` with one part:

| Part name              | Content-Type     | Content             |
|------------------------|------------------|---------------------|
| `addEcoNewsDtoRequest` | application/json | JSON-serialised DTO |

### DTO fields

| Field       | Type     | Required | Constraints                  |
|-------------|----------|----------|------------------------------|
| `title`     | string   | Yes      | 1 – 170 characters           |
| `text`      | string   | Yes      | min 20 characters            |
| `source`    | string   | No       | URL                          |
| `tags`      | string[] | Yes      | Non-empty; valid enum values |
| `imagePath` | string   | No       |                              |

Valid tag values: `NEWS`, `EVENTS`, `EDUCATION`, `INITIATIVES`, `ADS`
