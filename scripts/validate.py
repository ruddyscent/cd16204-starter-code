"""Run the completed project's local checks and save their text output."""

from pathlib import Path
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    evidence = root / "evidence"
    evidence.mkdir(exist_ok=True)
    checks = (
        [sys.executable, "-m", "pytest", "tests/"],
        [sys.executable, "-m", "flake8", "main.py", "starter/", "tests/",
         "scripts/", "inference_client.py"],
    )
    failed = False
    with (evidence / "validation.txt").open("w", encoding="utf-8") as log:
        for command in checks:
            heading = f"$ {' '.join(command)}\n"
            print(heading, end="", flush=True)
            log.write(heading)
            try:
                result = subprocess.run(
                    command, cwd=root, stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT, text=True, check=False,
                )
                output = result.stdout
                code = result.returncode
            except OSError as error:
                output = f"Unable to run check: {error}\n"
                code = 1
            print(output, end="", flush=True)
            log.write(output)
            status = f"Exit status: {code}\n\n"
            print(status, end="", flush=True)
            log.write(status)
            log.flush()
            failed = failed or code != 0
    return int(failed)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except OSError as error:
        print(f"Unable to write validation evidence: {error}", file=sys.stderr)
        sys.exit(1)
