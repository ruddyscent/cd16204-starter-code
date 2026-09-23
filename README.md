# Serving and Testing an ML Model with FastAPI

Complete this project in the supplied Udacity Workspace using local files and
commands. Build a Census income classifier, evaluate it, and serve predictions
through FastAPI. The training, inference, API, tests, and HTTP client are learner
exercises; this starter does not provide a completed solution.

Run commands from the repository root: the directory containing `requirements.txt`,
`main.py`, `setup.py`, `starter/`, and the supplied `data/census.csv`. Local Git is
optional. No GitHub/Azure account, remote push, DVC, cloud storage, hosted CI/CD,
public endpoint, or external runtime service is required. Package installation
requires network access; Udacity access and submission are still necessary.

## 1. Set up Python

Use Python 3.13 in the supplied Workspace (validated with 3.13.15). Python
3.12.3 is also validated for local Linux use. Create and activate a virtual
environment:

```sh
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip check
```

For local Python 3.12, substitute `python3.12` in both virtual-environment
creation commands in this guide. See [dependency notes](PYTHON_3_13_UPDATES.md)
for versions and verification limits. The requirements passed dependency smoke
checks in a clean virtual environment in the existing Linux Workspace with
Python 3.13.15 and previously on local Linux with Python 3.12.3. Fresh Workspace
image provisioning (issue #11) and completed-project end-to-end validation
(issue #16) remain separate checks.

## 2. Inspect and clean the supplied data

Load `data/census.csv` with pandas. Remove surrounding whitespace from column
names and string values, and decide how to handle missing-value markers such as
`?`. Preserve meaningful internal characters, original column names (including
`fnlgt` and hyphenated names), and the target `salary`. Do not remove every space
from the raw file indiscriminately. Keep the supplied CSV in the submission and
apply reproducible cleaning in code so an extracted project can use it.

## 3. Train, evaluate, and save inference artifacts

Complete `starter/train_model.py` and the unfinished functions in
`starter/ml/model.py`. Import preprocessing with
`from starter.ml.data import process_data`. Split the cleaned data into training
and held-out test sets before fitting preprocessing or the classifier. Fit the
encoder and label binarizer only on training data; reuse those fitted objects
for the test set and inference. Use a reproducible split.

Evaluate precision, recall, and F1 on the held-out set. Compute the same metrics
for categorical slices and save readable results, including each slice's sample
count, to root-level `slice_output.txt`. Explain empty or unsupported slices.

Use Python's `pickle` module to save the trained classifier and fitted objects
at these exact paths, creating `model/` when needed:

- `model/model.pkl`: trained classifier.
- `model/encoder.pkl`: fitted categorical encoder.
- `model/lb.pkl`: fitted label binarizer.

If your model requires additional fitted preprocessing, include it inside the
serialized classifier/pipeline or encoder artifact so these three files contain
all inference state. Preserve feature order and cleaning behavior between
training and serving. Load only your own trusted pickle artifacts.

Run training from the root after completing the implementation:

```sh
python -m starter.train_model
```

Copy `model_card_template.md` to `model_card.md` and complete it with the data,
model, held-out metrics, slice findings, intended use, and limitations. Record
any cleaning and feature choices needed to reproduce the model.

## 4. Implement the API and tests

Implement `app` in `main.py`. Load the saved artifacts without retraining on
startup or requests. Resolve artifact paths relative to the project files.

- `GET /`: HTTP 200 with a JSON welcome message; document its exact body.
- `POST /`: accept one record's features, excluding `salary`, and return HTTP
  200 with `{"prediction": "<=50K"}` or `{"prediction": ">50K"}`. Decode the
  predicted label using the fitted binarizer. Document the feature schema.
- Use typed Pydantic request fields and aliases for hyphenated Census names.
  Include a valid request example in the generated OpenAPI JSON.

Write at least three ML-function tests and three API tests under `tests/`, named
`test_*.py`. API tests must check the GET status and body and successful POST
status and prediction for both classes. Choose two inputs whose opposite
predictions you have confirmed with your fitted model; arbitrary fixed records
are not guaranteed to produce particular classes. Use FastAPI's TestClient.
Test preprocessing reuse, model behavior, and metrics with meaningful assertions.
Do not retrain the project model merely to load it for API tests.

## 5. Run local validation

```sh
python scripts/validate.py
```

This runs `python -m pytest tests/` followed by
`python -m flake8 main.py starter/ tests/ scripts/ inference_client.py` and writes
both outputs and exit statuses to `evidence/validation.txt`. Complete the HTTP
client in the next section before the final validation run. Both checks must
pass; incomplete starter files are expected to fail. The old `sanitycheck.py`
helper is not the validation or submission gate for this workflow.

## 6. Exercise the running server over real HTTP

Start the server in one activated terminal at the project root:

```sh
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Implement root-level `inference_client.py` with `requests`. It must use finite
request timeouts, print the URL, status, and response body, and exit nonzero on
connection errors or failed assertions. Against `http://127.0.0.1:8000`, it must:

1. Call `GET /` and assert HTTP 200 and the documented welcome body.
2. Call `POST /` with each of the two model-confirmed inputs, asserting HTTP 200
   and the expected opposite prediction labels. Print both request bodies.
3. Fetch `/openapi.json`, assert HTTP 200 and the presence of your request
   example(s), and save the JSON to `evidence/openapi.json`.

In a second activated terminal, run:

```sh
mkdir -p evidence
python inference_client.py > evidence/http.txt 2>&1
cat evidence/http.txt
python scripts/validate.py
```

Check the client command's exit status before running another command. Preserve
successful text evidence only after resolving failures. TestClient tests alone
do not establish real HTTP operation. OpenAPI JSON provides request-example
evidence without requiring Swagger UI, screenshots, or a CDN. Stop Uvicorn with
Ctrl-C when finished.

## 7. Package and verify the submission

Review source, documentation, and evidence for credentials or personal secrets
before packaging. Do not embed secrets in allowed files. Run:

```sh
python scripts/package_submission.py
python -m zipfile -l submission.zip
```

The packager requires the following exact root-relative files, and includes only
these plus non-hidden `.py` files recursively under `starter/` and `tests/`:

- `README.md`, `requirements.txt`, `setup.py`, `PYTHON_3_13_UPDATES.md`.
- `main.py`, `inference_client.py`, `starter/__init__.py`,
  `starter/train_model.py`, `starter/ml/__init__.py`, `starter/ml/data.py`,
  `starter/ml/model.py`, and at least one `tests/test_*.py` (possibly nested).
- `scripts/validate.py`, `scripts/package_submission.py`.
- `data/census.csv`.
- `model/model.pkl`, `model/encoder.pkl`, `model/lb.pkl`.
- `model_card.md`, `slice_output.txt`.
- `evidence/validation.txt`, `evidence/http.txt`, `evidence/openapi.json`.

Keep project Python helpers in `starter/`; the archive does not include arbitrary
root scripts, auxiliary data, or extra model files. Missing or empty required
files fail packaging (empty `__init__.py` markers are allowed). Symlinks in
selected paths or visible source trees are rejected. Environments, `.git`,
caches, hidden files, `.env`, credentials files, screenshots, prior archives,
and unrelated files outside the allowlist are excluded. Review the printed file
list; the packager cannot detect secrets embedded in source or evidence, nor
verify that learner results are correct. It refuses to overwrite an existing
`submission.zip`; move that archive aside before generating a replacement.

Extract into a new empty directory (choose a new path for each attempt):

```sh
python -m zipfile -e submission.zip /tmp/census-submission-check
cd /tmp/census-submission-check
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip check
python scripts/validate.py
```

Without running training, start Uvicorn and run the HTTP client again as in
section 6. Confirm that the extracted artifacts produce both expected classes
and the same API behavior. This verifies that no original working-directory
files or external runtime services are needed. If changes are needed, fix the
original project, regenerate evidence and ZIP, and repeat extraction.

Submit the self-contained `submission.zip` through the Udacity submission flow.
No repository URL, Git metadata, reviewer invitation, CI/CD screenshot, or
public URL is part of this project's submission contract.
