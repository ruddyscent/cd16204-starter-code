# Python environment and dependencies

Use Python 3.12 for the local Linux workflow. The dependency set was installed
and smoke-tested on CPython 3.12.3, Linux x86_64, in a clean virtual environment.
This replaces the earlier unverified Python 3.13 upgrade guidance; other Python
versions and the actual Udacity Workspace image have not been validated here.
`setup.py` declares Python 3.12 as the minimum; that declaration does not certify
every newer interpreter. No change to the learner implementation is required by
this dependency cleanup.

From the repository root:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip check
```

`requirements.txt` pins direct dependencies, preserving the previous compatible
versions and adding flake8. It is not a complete transitive lockfile; record
`python --version` and `python -m pip freeze` with validation evidence. Install
requirements before the editable package: `setup.py` supplies local package
metadata, not a second dependency list.

## Retained direct dependencies

| Package | Version | Purpose |
| --- | --- | --- |
| numpy | 2.3.3 | Arrays used by supplied preprocessing and ML functions. |
| pandas | 2.3.2 | Census CSV loading, tabular preprocessing, and categorical slices. |
| scikit-learn | 1.7.2 | Encoders, train/test split, classifier training, and metrics. |
| fastapi | 0.117.1 | Learner GET/POST API and OpenAPI generation. |
| pydantic | 2.11.9 | Typed request bodies, aliases, and examples. |
| uvicorn | 0.36.0 | Local HTTP server for the completed API. |
| httpx | 0.28.1 | HTTP client required by FastAPI/Starlette TestClient. |
| requests | 2.32.5 | Separate real HTTP requests to the running server. |
| pytest | 8.4.2 | Learner ML and API tests. |
| flake8 | 7.3.0 | Local Python lint validation. |

## Removed dependencies

Inspection of the supplied Python imports and retained project exercises found
no use of Aequitas, Altair, Flask, Flask-Bootstrap, matplotlib, seaborn,
Jupyter, ipykernel, nbformat, httplib2, python-multipart, or pytest-asyncio.
Categorical slice metrics use pandas and scikit-learn; they do not require a
fairness dashboard or plots. The API accepts JSON, not multipart forms, and
synchronous TestClient tests do not require an asynchronous pytest plugin.
Notebook tooling is not part of the required command-line workflow.

Uvicorn's optional `standard` extras were removed: the required plain HTTP
server works with its base dependencies; WebSockets, reload acceleration, and
optional configuration formats are not required. No cloud SDK or replacement
external runtime service was added.

## Verification boundary

A clean Linux environment passed dependency installation, editable installation,
`pip check`, imports, scratch preprocessing/classifier/serialization/metrics
checks, FastAPI/Pydantic alias and OpenAPI checks through TestClient, and a real
requests call to a scratch Uvicorn server. Scratch pytest and flake8 commands
also passed. These probes check dependency interoperability, not the learner's
solution, and are not committed project regression tests.

The starter training and inference functions and API remain exercises. This
verification does not establish that completed-project tests or repository-wide
lint pass, that Census training works end to end, or that a fresh Udacity
Workspace has been validated.
