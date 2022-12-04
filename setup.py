from pathlib import Path

from setuptools import find_packages, setup


def read_requirements(path):
    return list(Path(path).read_text().splitlines())

setup(
    name="FogML",
    version="0.0.5",
    description="Source code generators for machine learning models",
    license="Apache License 2.0",
    packages=find_packages(),
    install_requires=read_requirements("requirements.txt"),
    python_requires=">=3.7",
)
