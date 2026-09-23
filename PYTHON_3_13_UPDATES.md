# Python environment and dependencies

Use Python 3.13 in the supplied Udacity Workspace. The ten direct dependencies
were installed and smoke-tested in a clean virtual environment on the existing
Workspace's Linux x86_64 runtime with Python 3.13.15. The earlier clean local
Linux x86_64 validation on CPython 3.12.3 also remains applicable to these pins.
`setup.py` declares Python 3.12 as the minimum; that declaration does not certify
every newer interpreter. Other Python versions and platforms have not been
validated here. No change to the learner implementation is required by this
dependency cleanup.

From the repository root:

```sh
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip check
```

For local Python 3.12, use `python3.12` to create the environment instead.

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

The existing Udacity Workspace passed installation of all ten pins in a new
isolated virtual environment, editable package installation, `pip check`, and
imports of the supplied preprocessing and metrics. Three temporary dependency
probes passed: pandas/NumPy/scikit-learn interoperability on synthetic data,
FastAPI/Pydantic request validation and OpenAPI access through httpx TestClient,
and a real loopback requests call to a scratch Uvicorn server. Flake8 passed on
the temporary probe file. The probes reported one unsuppressed warning about
Starlette TestClient's use of the deprecated `anyio.abc.BlockingPortal` alias.

The earlier local Python 3.12.3 validation passed dependency and editable
installation, `pip check`, imports, scratch preprocessing/classifier/
serialization/metrics checks, FastAPI/Pydantic alias and OpenAPI checks through
TestClient, and a real requests call to a scratch Uvicorn server. Scratch pytest
and flake8 commands also passed in that environment.

These probes check dependency interoperability, not the learner's solution, and
are not committed project regression tests. The starter training and inference
functions and API remain exercises. Neither validation establishes that
completed-project tests or repository-wide lint pass, that Census training
works end to end, or that submission extraction and real HTTP inference with
learner artifacts succeed. Existing-Workspace dependency setup is distinct from
fresh Workspace image provisioning (issue #11) and completed-project end-to-end
validation (issue #16); those checks remain separate.
