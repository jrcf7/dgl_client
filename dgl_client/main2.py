import typer
from typing_extensions import Annotated
from loguru import logger
import os
import sys
from .api_cli import APIClient, InferenceClient
import uuid
from glob import glob
import json
from rich import print


from .commands.chat import app as chat
from .commands.collections import app as coll
from .commands.ls import app as ls

app = typer.Typer()
app.add_typer(ls, name="ls")
app.add_typer(chat, name="chat")
app.add_typer(coll, name="collection")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    Example of a CLI app with two subcommands imported from external modules
    """
    if ctx.invoked_subcommand is None:
        print(f"About to execute command: {ctx.invoked_subcommand}")

def do_run():
    LOGDIR="./logs"
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)

    logger.add(os.path.join(LOGDIR, "file_{time}.log"))

    app()

if __name__ == "__main__":
    do_run()