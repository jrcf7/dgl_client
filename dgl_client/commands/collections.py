import typer
from rich import print
import logging

logger = logging.getLogger(__name__)

from .utils import get_back_client, do_login, DGL_BCK_ENDPOINT

app = typer.Typer()

@app.command("create")
def create_collection(
  name: str,
  descr: str,
  bucket: str|None = None,
  access_key: str = typer.Option(help="The authorization key"),
  endpoint: str = typer.Option(default=DGL_BCK_ENDPOINT,help="The main endpoint of the system"),
  inference_url: str = typer.Option(default="api/v1/"),
  ):
    client = get_back_client(endpoint, inference_url)    
    if (client.login(access_key)):
        coll = client.create_collection(
            name = name,
            descr = descr,
            bucket = bucket if bucket != None else name
        )
        if coll:
            print(coll)
    else:
        logger.error("Login failed")
        typer.Exit(-1)

@app.command("upload")
def upload_dcoment(
  cid: str,
  path: str,
  access_key: str = typer.Option(help="The authorization key"),
  endpoint: str = typer.Option(default=DGL_BCK_ENDPOINT,help="The main endpoint of the system"),
  inference_url: str = typer.Option(default="api/v1/"),
  ):
    client = get_back_client(endpoint, inference_url)    
    if (client.login(access_key)):
        coll = client.upload_document(
            cid = cid,
            path = path,
        )
        if coll:
            print(coll)
    else:
        logger.error("Login failed")
        typer.Exit(-1)

@app.command("ls")
def list_collections(
  access_key: str = typer.Option(help="The authorization key"),
  endpoint: str = typer.Option(default=DGL_BCK_ENDPOINT),
  inference_url: str = typer.Option(default="api/v1/"),
  ):
    client = get_back_client(endpoint, inference_url)    
    if (client.login(access_key)):
        collections = client.get_collections()
        for coll in collections:
            print("* %s: %s - %s"%(coll["id"],coll["frontend_collection_id"],coll["title"]))
    else:
        logger.error("Login failed")
        typer.Exit(-1)

@app.command("lsd")
def list_documents(
  cid: str, 
  access_key: str = typer.Option(help="The authorization key"),
  endpoint: str = typer.Option(default=DGL_BCK_ENDPOINT),
  inference_url: str = typer.Option(default="api/v1/"),
  ):
    client = get_back_client(endpoint, inference_url)    
    if (client.login(access_key)):
        documents = client.get_documents(cid)
        print(documents)
        # for doc in documents:
        #     print(doc)
    else:
        logger.error("Login failed")
        typer.Exit(-1)       

@app.command("download")
def download_document(
  cid: str, 
  did: str,
  filename: str = typer.Option(help="File name to save to"),
  access_key: str = typer.Option(help="The authorization key"),
  endpoint: str = typer.Option(default=DGL_BCK_ENDPOINT),
  inference_url: str = typer.Option(default="api/v1/"),
  ):
    client = get_back_client(endpoint, inference_url)    
    if (client.login(access_key)):
        client.download_document(cid, did, filename)
    else:
        logger.error("Login failed")
        typer.Exit(-1)           