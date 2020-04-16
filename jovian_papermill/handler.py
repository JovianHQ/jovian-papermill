import os

from requests import get

from .jovian_utils import _h, upload_file
from .utils import add_parameters_tag, get_gist_and_nbfile, get_nbfile, log


class JovianHandler:
    gist = None
    creds = None

    @classmethod
    def read(cls, path):
        """
        Read a notebook from Jovian
        """
        gist, nbfile, creds = get_gist_and_nbfile(path)
        cls.gist = gist
        cls.creds = creds

        log(f"Cloning...")
        notebook = get(nbfile["rawUrl"]).content
        return add_parameters_tag(notebook)

    @classmethod
    def write(cls, file_content, path):
        """
        Commit a notebook to Jovian
        """
        gist_slug = cls.gist["slug"]
        filename = get_nbfile(cls.gist["files"])["filename"]

        log(f"Committing...")
        upload_file(
            gist_slug=gist_slug, file=(filename, file_content), creds=cls.creds,
        )

    @classmethod
    def pretty_path(cls, path):
        return path

    @classmethod
    def listdir(cls, path):
        raise NotImplementedError
