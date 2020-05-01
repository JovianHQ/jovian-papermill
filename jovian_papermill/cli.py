import os
import json
import click

from jovian_papermill._version import __version__
from jovian_papermill.execute import execute
from jovian_papermill.utils import log


@click.group()
@click.version_option(version=__version__, prog_name="jovian-papermill")
@click.pass_context
def main(ctx, log_level="info"):
    """Parametrize and Execute notebooks with Jovian-Papermill"""
    pass


@main.command("execute", short_help="Execute Papermill jobs")
@click.argument("gist")
@click.option('-p', '--parameters-file', 'parameters_file', help="Path to parameters file",
              type=click.File('rb'),
              default=None,
              required=True)
@click.option('-v', '--version', 'version', help="Gist version", type=str, default='0')
@click.pass_context
def execute_cli(ctx, gist, parameters_file, version):
    try:
        API_KEY = os.environ["JOVIAN_API_KEY"]
        API_URL = os.environ["JOVIAN_API_URL"]
    except KeyError:
        log("Please provide JOVIAN_API_KEY and JOVIAN_API_URL as environment variables", error=True)
        return

    creds = {
        "API_KEY": API_KEY,
        "API_URL": API_URL
    }

    log("Reading parameters...")
    parameters_list = json.loads(parameters_file.read()).get("parameters")

    if not parameters_list or not isinstance(parameters_list, list):
        raise ValueError("parameters not passed in correct format")

    log("Executing..")
    for idx, parameters in enumerate(parameters_list):
        log("Executing parameters: {}".format(idx + 1))

        execute(gist=gist, parameters=parameters, creds=creds, version=version)

    log("Success!")


if __name__ == '__main__':
    main()
