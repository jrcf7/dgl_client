import typer
from typing_extensions import Annotated
import logging
import os
import sys
from .api_cli import APIClient, InferenceClient
import uuid
from glob import glob
import json
from rich import print

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


from .commands.chat import app as chat
from .commands.collections import app as coll
from .commands.ls import app as ls

app = typer.Typer()
app.add_typer(ls, name="ls")
app.add_typer(chat, name="chat")
app.add_typer(coll, name="collection")

@app.callback(
    invoke_without_command=True,
    context_settings={
        "allow_extra_args": True, 
        "ignore_unknown_options": True
        }
    )
def main(ctx: typer.Context):
    """
    Example of a CLI app with two subcommands imported from external modules
    """
    print(ctx.args)
    if ctx.invoked_subcommand is None:
        print(f"About to execute command: {ctx.invoked_subcommand}")

if __name__ == "__main__":
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] - [%(filename)s > %(funcName)s() > %(lineno)s] %(message)s")
    LOGDIR="./logs"
    if not os.path.exists(LOGDIR):
        os.makedirs(LOGDIR)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)

    fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", str(uuid.uuid4())))
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)    

    app()