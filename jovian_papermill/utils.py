import base64
import json
import re
from urllib.parse import parse_qs, urlparse

import nbformat

from .jovian_utils import get_gist


def log(msg):
    print(f"[jovian-papermill] {msg}")


def get_nbfile(files):
    """Find and return notebook file"""
    for file in files:
        if "language" in file and file["language"] == "Jupyter Notebook":
            return file
    return None


def get_slug_and_version(path):
    parsed_url = urlparse(path)

    slug = parsed_url.path[1:]
    query = parse_qs(parsed_url.query)

    version = query["gist_version"][0]
    creds = decode(query["creds"][0])

    return slug, version, creds


def get_gist_and_nbfile(path):
    """Get gist and nbfile from custom Jovian path
    
    Arguments
        path
            - should be in the form of jovian:///gist_slug?gist_version=2
    Returns
        gist, nbfile
    """
    slug, version, creds = get_slug_and_version(path)
    gist = get_gist(slug, version, creds)
    nbfile = get_nbfile(gist["files"])

    return gist, nbfile, creds


def add_parameters_tag(notebook):
    """Add tag 'parameters' to notebook cell containing the '# parametrize'"""
    nb = nbformat.reads(notebook, as_version=4)
    # Check if the tag 'parameters' already exists in any of the cells
    for cell in nb.cells:
        if "tags" in cell.metadata and "parameters" in cell.metadata["tags"]:
            return json.dumps(nb)

    pattern = re.compile("^# *parametrize", re.IGNORECASE)

    # Find the first cell containing '# parametrize'
    param_cell = None
    for cell in nb.cells:
        if pattern.match(cell.source):
            param_cell = cell
            break

    if (
        param_cell
        and "tags" in param_cell.metadata
        and "parameters" not in param_cell.metadata["tags"]
    ):
        param_cell.metadata["tags"].append("parameters")
        log("Added tag 'parameters'")

    elif param_cell and "tags" not in param_cell.metadata:
        param_cell.metadata.update({"tags": ["parameters"]})
        log("Added tag 'parameters'")

    elif not param_cell:
        raise Exception(
            "Input notebook does not contain a cell with comment '# parametrize'"
        )

    return json.dumps(nb)


def encode(creds):
    return base64.b64encode(json.dumps(creds).encode("utf-8")).decode("utf-8")


def decode(creds):
    return json.loads(base64.b64decode(creds).decode("utf-8"))
