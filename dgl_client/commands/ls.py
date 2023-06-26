import typer
from rich import print
from typing import Optional
from loguru import logger
from .utils import get_inf_client, do_login, DGL_INF_ENDPOINT

app = typer.Typer()

def list_models(client):
  available_models = client.get_available_models()
  logger.info("Available models %s"%str(available_models))

  available_wkf = client.get_available_workflows()
  logger.info("Available workflows %s"%str(available_wkf))

  return available_models, available_wkf

def list_chats(client, access_key):
  do_login(access_key, client)
  chats = client.list_chats()
  logger.info("Found %d existing chats"%(len(chats)))

  for chat in chats:
    print("* %s - %s"%(chat[0],chat[1][:25]))

  return chats

def list_messages(client, access_key, chat_id):
  do_login(access_key, client)
  messages = client.list_messages(chat_id)
  logger.info("Found %d existing chats"%(len(messages)))

  for message in messages:
    print(message)

  return messages

@app.callback(invoke_without_command=True)
def ls(
  resource: str,
  endpoint: str = typer.Option(default=DGL_INF_ENDPOINT),
  inference_url: str = typer.Option(default="/inference/"),
  ):
    client = get_inf_client(endpoint, inference_url)

    match resource:
        case "models":
            list_models(client)
        case "model":
            list_models(client)      
        case "chats":
            list_chats(client)            
        # case "messages":
        #     if args.chat_id:
        #         list_messages(client, args.chat_id)
        case _:
            logger.error("Resource not found!")
