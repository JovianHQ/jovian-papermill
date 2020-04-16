import json

import nbformat
import pytest

from jovian_papermill.utils import add_parameters_tag


@pytest.mark.parametrize(
    "source",
    [
        ["#parametrize\n"],
        ["# Parametrize\n"],
        ["#  PaRaMeTrIZE\n"],
        ["#    parametrize\n"],
        ["#    parametrize\n"],
    ],
)
def test_add_parameters_tag(source):
    with open("jovian_papermill/tests/resources/notebook1.ipynb") as f:
        nb = nbformat.read(f, as_version=4)
        nb.cells[0]["source"] = source
        nb = nbformat.NotebookNode(json.loads(add_parameters_tag(json.dumps(nb))))
        assert "parameters" in nb.cells[0]["metadata"]["tags"]


@pytest.mark.parametrize(
    "source",
    [
        ["# prametrize\n"],
        ["parametrize\n"],
        ["parametriz\n"],
        ["#123parametriz\n"],
        ["print('Hello world') # parametrize\n"],
        ["123# parametrize\n"],
        ["hello# Parametrize\n"],
    ],
)
def test_add_parameters_tag_raises_exception(source):
    with open("jovian_papermill/tests/resources/notebook1.ipynb") as f:
        nb = nbformat.read(f, as_version=4)
        nb.cells[0]["source"] = source

        with pytest.raises(Exception):
            nb = nbformat.NotebookNode(json.loads(add_parameters_tag(json.dumps(nb))))
