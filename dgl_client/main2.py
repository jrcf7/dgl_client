import typer
from typing_extensions import Annotated
import logging
import os
import sys
from .api_cli import APIClient
import uuid
from glob import glob
import json

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] - [%(filename)s > %(funcName)s() > %(lineno)s] %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
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

app = typer.Typer()
chat_app = typer.Typer()
app.add_typer(chat_app, name="chat")
coll_app = typer.Typer()
app.add_typer(coll_app, name="coll")
ls_app = typer.Typer()
app.add_typer(ls_app, name="ls")


@chat_app.command("message")
def char_message(item: str,
):
    print(f"Creating item: {item}")


if __name__ == "__main__":
    app()