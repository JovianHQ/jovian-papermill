"""Utility functions for Jovian"""
from requests import get, post


def _msg(res):
    try:
        data = res.json()
        if "errors" in data and len(data["errors"]) > 0:
            return data["errors"][0]["message"]
        if "message" in data:
            return data["message"]
        if "msg" in data:
            return data["msg"]
    except:
        if res.text:
            return res.text
        return "Something went wrong"


def pretty(res):
    """Make a human readable output from an HTML response"""
    return "(HTTP " + str(res.status_code) + ") " + _msg(res)


def urljoin(*args):
    """Join multiple url parts to construct one url"""
    if len(args) == 0:
        raise TypeError("urljoin requires at least one argument")

    trailing_slash = "/" if args[-1].endswith("/") else ""

    return "/".join(map(lambda x: str(x).strip("/"), args)) + trailing_slash


def _u(api_url, path):
    """Make a URL from the path"""
    return urljoin(api_url, path)


def _v(version):
    """Create version query parameter string"""
    if version is not None:
        return "?gist_version=" + str(version)
    return ""


def _h(api_key):
    headers = {}
    if api_key is not None:
        headers["Authorization"] = "Bearer " + api_key
    return headers


def get_gist(slug, version, creds):
    """Download a gist"""

    if "/" in slug:
        parts = slug.split("/")
        username, title = parts[0], parts[1]
        url = _u(creds["API_URL"], "user/" + username + "/gist/" + title + _v(version))
    else:
        url = _u(creds["API_URL"], "gist/" + slug + _v(version))

    res = get(url, headers=_h(creds["API_KEY"]))
    if res.status_code == 200:
        return res.json()["data"]
    raise Exception("Failed to retrieve Gist: " + str(res))


def upload_file(
    gist_slug,
    file,
    creds,
    folder=None,
    version=None,
    artifact=False,
    version_title=None,
):
    """Upload an additional file to a gist"""
    data = {"artifact": "true"} if artifact else {}
    if folder:
        data["folder"] = folder
    if version_title:
        data["version_title"] = version_title

    res = post(
        url=_u(creds["API_URL"], "/gist/" + gist_slug + "/upload" + _v(version)),
        files={"files": file},
        data=data,
        headers=_h(creds["API_KEY"]),
    )
    if res.status_code == 200:
        return res.json()["data"]
    raise Exception("File upload failed: " + pretty(res))
