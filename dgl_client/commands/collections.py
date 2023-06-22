import typer
from rich import print
import logging

logger = logging.getLogger(__name__)

from .utils import get_back_client, do_login, DGL_API_ENDPOINT

app = typer.Typer()

@app.command("create")
def create_collection(
  access_key: str,
  endpoint: str = typer.Option(default=DGL_API_ENDPOINT),
  inference_url: str = typer.Option(default="api/v1/"),
  ):
    client = get_back_client(endpoint, inference_url)

@app.command("ls")
def list_collections(
  access_key: str,
  endpoint: str = typer.Option(default=DGL_API_ENDPOINT),
  inference_url: str = typer.Option(default="api/v1/"),
  ):
    client = get_back_client(endpoint, inference_url)    
    if (client.login(access_key)):
        collections = client.get_collections()
        for coll in collections:
            print("* %s - %s"%(coll["id"],coll["title"]))
    else:
        logger.error("Login failed")
        typer.Exit(-1)