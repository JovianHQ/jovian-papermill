from urllib.parse import parse_qs, urlparse
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
