import setuptools

setuptools.setup(
    name="starter",
    version="0.0.0",
    description="Starter code.",
    author="Student",
    python_requires=">=3.12",
    packages=setuptools.find_packages(include=["starter", "starter.*"]),
)
