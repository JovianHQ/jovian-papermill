import warnings

warnings.filterwarnings("ignore")
import papermill as pm
from .utils import log


def execute(gist_slug, parameters, version="0"):
    path = f"jvn:///{gist_slug}?gist_version={version}"
    pm.execute_notebook(
        path,
        path,
        parameters=parameters,
        request_save_on_cell_execute=False,
        progress_bar=False,
        log_level="INFO",
    )
