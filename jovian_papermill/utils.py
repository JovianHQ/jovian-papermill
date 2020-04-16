from urllib.parse import parse_qs, urlparse


def log(msg):
    print(f"[jovian-papermill]: {msg}")


def get_nbfile(files):
    """Find and return notebook file"""
    for file in files:
        if "language" in file and file["language"] == "Jupyter Notebook":
            return file
    return None


def get_slug_and_version(path):
    """Get slug and version from custom Jovian path
    
    Arguments
        path
            - should be in the form of jvn:///gist_slug?gist_version=2
    Returns
        slug, version
    """
    parsed_url = urlparse(path)

    slug = parsed_url.path[1:]
    query = parse_qs(parsed_url.query)

    version = 0
    if "gist_version" in query:
        version = query["gist_version"][0]

    return slug, version
