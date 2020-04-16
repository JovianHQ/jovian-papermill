import warnings

warnings.filterwarnings("ignore")
try:
    import papermill as pm
except:
    pass
from .utils import log


def execute(gist_slug, parameters, version="0"):
    path = f"jovian:///{gist_slug}?gist_version={version}"
    pm.execute_notebook(
        input_path=path,
        output_path=path,
        parameters=parameters,
        request_save_on_cell_execute=False,
        progress_bar=False,
        log_level="INFO",
    )
    log("Done!")
