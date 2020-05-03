import os

import requests_cache
import requests

from .jovian_utils import _h, upload_file
from .utils import add_parameters_tag, get_gist_and_nbfile, get_nbfile, log

requests_cache.install_cache('jovian_papermill_cache')


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

        notebook = requests.get(nbfile["rawUrl"]).content
        return add_parameters_tag(notebook)

    @classmethod
    def write(cls, file_content, path):
        """
        Commit a notebook to Jovian
        """
        if cls.gist is None or cls.creds is None:
            gist, nbfile, creds = get_gist_and_nbfile(path)
            cls.gist = gist
            cls.creds = creds

        gist_slug = cls.gist["slug"]
        nbfilename = get_nbfile(cls.gist["files"])["filename"]

        res = upload_file(
            gist_slug=gist_slug, file=(
                nbfilename, file_content), creds=cls.creds,
        )
        slug, version = res["slug"], res["version"]
        # Upload remaining files
        for file in cls.gist["files"]:
            if file["filename"] != nbfilename:
                upload_file(
                    gist_slug=gist_slug,
                    file=(file["filename"], requests.get(
                        file["rawUrl"]).content),
                    creds=cls.creds,
                    version=version
                )

    @classmethod
    def pretty_path(cls, path):
        return path

    @classmethod
    def listdir(cls, path):
        raise NotImplementedError
