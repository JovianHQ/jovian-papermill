import os
import warnings

import papermill as pm

from .utils import encode, log

warnings.filterwarnings("ignore")


def execute(gist, parameters, creds, version="0", input_path=None, **kwargs):
    creds = encode(creds)
    path = f"jovian:///{gist}?gist_version={version}&creds={creds}"

    pm.execute_notebook(
        input_path=input_path if input_path else path,
        output_path=path,
        parameters=parameters,
        request_save_on_cell_execute=False,
        progress_bar=False,
        log_level="INFO",
        **kwargs
    )
