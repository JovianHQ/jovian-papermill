""""
setup.py
See:
https://packaging.python.org/tutorials/packaging-projects/
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""
import os

from setuptools import find_packages, setup

local_path = os.path.dirname(__file__)
# Fix for tox which manipulates execution pathing
if not local_path:
    local_path = "."
here = os.path.abspath(local_path)


def read(fname):
    with open(fname, "r") as fhandle:
        return fhandle.read()


def read_reqs(fname):
    req_path = os.path.join(here, fname)
    return [req.strip() for req in read(req_path).splitlines() if req.strip()]


# Get the long description from the README file
with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="jovian_papermill",
    version="0.0.0",
    author="Jovian",
    author_email="hello@jovian.ml",
    description="A Jovian I/O handler for papermill",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JovianML/jovian-papermill",
    packages=find_packages(),
    python_requires=">=3.5",
    install_requires=read_reqs("requirements.txt"),
    entry_points={"papermill.io": [r"jovian://=jovian_papermill:JovianHandler"]},
    project_urls={
        "Source": "https://github.com/JovianML/jovian-papermill/",
        "Tracker": "https://github.com/JovianML/jovian-papermill/issues",
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
