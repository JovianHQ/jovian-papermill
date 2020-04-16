from requests import get

from jovian.utils import api, clone
from .utils import get_nbfile, get_slug_and_version, log


class JovianHandler:
    @classmethod
    def read(cls, path):
        """
        Read a notebook from Jovian
        """
        slug, version = get_slug_and_version(path)
        gist = clone.get_gist(slug, version, fresh=False)
        nbfile = get_nbfile(gist["files"])
        notebook = get(nbfile["rawUrl"]).content
        log(f"Cloned {slug}")
        return notebook

    @classmethod
    def write(cls, file_content, path):
        """
        Commit a notebook to Jovian
        """
        slug, _ = get_slug_and_version(path)
        metadata = api.get_gist(slug)
        filename = get_nbfile(metadata["files"])["filename"]
        gist_slug = metadata["slug"]

        api.upload_file(gist_slug=gist_slug, file=(filename, file_content))
        log(f"Committed to {slug}")

    @classmethod
    def pretty_path(cls, path):
        return path

    @classmethod
    def listdir(cls, path):
        raise NotImplementedError
