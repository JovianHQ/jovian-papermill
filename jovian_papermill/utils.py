import json
import re
from urllib.parse import parse_qs, urlparse

import nbformat
from jovian.utils import clone


def log(msg):
    print(f"[jovian-papermill] {msg}")


def get_nbfile(files):
    """Find and return notebook file"""
    for file in files:
        if "language" in file and file["language"] == "Jupyter Notebook":
            return file
    return None


def get_gist_and_nbfile(path):
    """Get gist and nbfile from custom Jovian path
    
    Arguments
        path
            - should be in the form of jovian:///gist_slug?gist_version=2
    Returns
        gist, nbfile
    """
    parsed_url = urlparse(path)

    slug = parsed_url.path[1:]
    query = parse_qs(parsed_url.query)

    version = 0
    if "gist_version" in query:
        version = query["gist_version"][0]

    gist = clone.get_gist(slug, version, fresh=False)
    nbfile = get_nbfile(gist["files"])

    return gist, nbfile


def add_metadata(notebook):
    """Add tag 'parameters' to notebook cell containing the '# parametrize'"""
    nb = nbformat.reads(notebook, as_version=4)

    pattern = re.compile("# *parametrize", re.IGNORECASE)

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
