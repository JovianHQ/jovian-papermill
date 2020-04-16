from requests import get

from jovian.utils import api, clone
from .utils import get_nbfile, get_gist_and_nbfile, add_metadata, log


class JovianHandler:
    gist = None

    @classmethod
    def read(cls, path):
        """
        Read a notebook from Jovian
        """
        gist, nbfile = get_gist_and_nbfile(path)
        cls.gist = gist

        log(f"Cloning...")
        notebook = get(nbfile["rawUrl"]).content
        return add_metadata(notebook)

    @classmethod
    def write(cls, file_content, path):
        """
        Commit a notebook to Jovian
        """
        gist_slug = cls.gist["slug"]
        filename = get_nbfile(cls.gist["files"])["filename"]

        log(f"Committing...")
        api.upload_file(gist_slug=gist_slug, file=(filename, file_content))

    @classmethod
    def pretty_path(cls, path):
        return path

    @classmethod
    def listdir(cls, path):
        raise NotImplementedError
