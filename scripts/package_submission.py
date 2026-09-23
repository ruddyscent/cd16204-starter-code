"""Package the documented submission files without traversing symlinks."""

from pathlib import Path
import sys
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


REQUIRED = (
    "README.md", "requirements.txt", "setup.py", "PYTHON_3_13_UPDATES.md",
    "main.py", "inference_client.py", "starter/__init__.py",
    "starter/train_model.py", "starter/ml/__init__.py", "starter/ml/data.py",
    "starter/ml/model.py", "scripts/validate.py",
    "scripts/package_submission.py",
    "data/census.csv", "model/model.pkl", "model/encoder.pkl", "model/lb.pkl",
    "model_card.md", "slice_output.txt", "evidence/validation.txt",
    "evidence/http.txt", "evidence/openapi.json",
)


def checked_file(root, relative):
    path = root / relative
    for component in (path, *path.parents):
        if component == root:
            break
        if component.is_symlink():
            raise ValueError(f"Symlinks are not allowed: {relative}")
    if not path.is_file():
        raise ValueError(f"Required file missing: {relative}")
    if path.stat().st_size == 0 and path.name != "__init__.py":
        raise ValueError(f"Required file missing or empty: {relative}")
    return path


def python_sources(root, directory):
    base = root / directory
    if base.is_symlink() or not base.is_dir():
        raise ValueError(f"Expected a real source directory: {directory}")
    # Environments may have arbitrary, non-hidden names inside source trees.
    if ((base / "pyvenv.cfg").exists()
            or (base / "conda-meta").is_dir()
            or ((base / "bin/activate").is_file()
                and any((base / "lib").glob("python*/site-packages")))
            or ((base / "Scripts/activate.bat").is_file()
                and (base / "Lib/site-packages").is_dir())):
        return []
    files = []
    for path in sorted(base.iterdir()):
        if path.name.startswith(".") or path.name == "__pycache__":
            continue
        if path.is_symlink():
            relative = path.relative_to(root)
            raise ValueError(f"Symlinks are not allowed: {relative}")
        if path.is_dir():
            files.extend(python_sources(root, path.relative_to(root)))
        elif path.suffix == ".py":
            files.append(path.relative_to(root).as_posix())
    return files


def main():
    root = Path(__file__).resolve().parents[1]
    names = set(REQUIRED)
    names.update(python_sources(root, "starter"))
    tests = python_sources(root, "tests")
    if not any(Path(name).name.startswith("test_") for name in tests):
        raise ValueError("tests/ must include at least one test_*.py file")
    names.update(tests)
    for name in names:
        checked_file(root, name)
    output = root / "submission.zip"
    if output.exists() or output.is_symlink():
        raise ValueError("submission.zip exists; move it before packaging")
    with tempfile.TemporaryDirectory(prefix="submission-") as temp:
        archive = Path(temp) / "submission.zip"
        with ZipFile(archive, "w", compression=ZIP_DEFLATED) as bundle:
            for name in sorted(names):
                info = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                bundle.writestr(info, (root / name).read_bytes())
        with output.open("xb") as target:
            target.write(archive.read_bytes())
    print(f"Created {output} with {len(names)} files:")
    print("\n".join(sorted(names)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Packaging failed: {error}", file=sys.stderr)
        sys.exit(1)
