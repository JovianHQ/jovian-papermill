from requests import get

from jovian.utils import api, clone
from jovian_papermill.utils import get_nbfile, get_slug_and_version


class JovianHandler:
    @classmethod
    def read(self, path):
        """
        Read a notebook from a Jovian server.
        """
        slug, version = get_slug_and_version(path)

        gist = clone.get_gist(slug, version, fresh=False)
        nbfile = get_nbfile(gist["files"])
        notebook = get(nbfile["rawUrl"]).content

        return notebook

    @classmethod
    def write(self, file_content, path):
        """
        Commit a notebook to a Jovian server.
        """
        slug, version = get_slug_and_version(path)

        metadata = api.get_gist(slug, version)
        filename = get_nbfile(metadata["files"])["filename"]

        f = (filename, file_content)
        api.upload_file(gist_slug=slug, file=f)

    @classmethod
    def pretty_path(self, path):
        return path

    @classmethod
    def listdir(self, path):
        raise NotImplementedError
