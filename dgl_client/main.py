import argparse
import logging
import os
import sys
from .api_cli import APIClient, prepare_token
import uuid
from glob import glob
import json

logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] - [%(filename)s > %(funcName)s() > %(lineno)s] %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_client(args):
  logger.info("Connecting to API Endpoint %s"%args.endpoint)
  client = APIClient(args.endpoint)    
  return client

def list_models(args):
  client = get_client(args)
  available_models = client.get_available_models()
  logger.info("Available models %s"%str(available_models))

  available_wkf = client.get_available_workflows()
  logger.info("Available workflows %s"%str(available_wkf))

  return available_models, available_wkf

def list_chats(args):
  client = get_client(args)
  do_login(args, client)
  chats = client.list_chats()
  logger.info("Found %d existing chats"%(len(chats)))

  for chat in chats:
    print("* %s - %s"%(chat[0],chat[1][:25]))

  return chats

def list_messages(args, chat_id):
  client = get_client(args)
  do_login(args, client)
  messages = client.list_messages(chat_id)
  logger.info("Found %d existing chats"%(len(messages)))

  for message in messages:
    print(message)

  return messages

def main_ls(args):
  match args.resource:
    case "models":
      list_models(args)
    case "model":
      list_models(args)      
    case "chats":
      list_chats(args)            
    case "messages":
      if args.chat_id:
        list_messages(args, args.chat_id)
    case _:
      logger.error("Resource not found!")

def do_login(args, client):
  if args.access_key:
    client.login(args.access_key)
    return True

  return False

def main_chat(args):
  client = get_client(args)

  model_config_name = args.model

  do_login(args, client)

  if args.chat_id:
    chat_id = client.continue_chat(args.chat_id)
  else:
    chat_id = client.create_chat()

  logger.info(f"Chat ID: {chat_id}")

  message = args.message

  events = client.send_message(message, model_config_name)

  print()
  print("You: %s"%(message))
  print()
  print("Assistant: ", end="", flush=True)
  ass_reply = []
  for event in events:
      print(event, end="", flush=True)
      ass_reply.append(event)
  print()
  return ass_reply

def main():
  DGL_API_ENDPOINT = "https://www.diglife.eu/inference"
  if "DGL_API_ENDPOINT" in os.environ and os.environ["DGL_API_ENDPOINT"]:
    DGL_API_ENDPOINT = os.environ["DGL_API_ENDPOINT"]

  parser = argparse.ArgumentParser(description='DigLife API Client.')
  parser.add_argument('--logdir', type=str, default="logs/",
                      help='Where to store logs')
  parser.add_argument('--endpoint', type=str, default=DGL_API_ENDPOINT,
                      help='Endpoint for the inference')
  parser.add_argument('-k','--access_key', type=str, required=True,
                      help='Access keys to authenticate to the API')                      
  parser.add_argument('-c','--chat-id', type=str,
                      help='Continue previous chat')

  subparsers = parser.add_subparsers(help='You can choose between different commands')
  chat_p = subparsers.add_parser('chat', help='chat with the assistants')
  chat_p.set_defaults(func=main_chat)

  chat_p.add_argument('message', type=str, 
                      help='say something to the model')
  chat_p.add_argument('-m','--model', type=str, required=True,
                      help='Which model do you want to talk to?')
  chat_p.add_argument('-i','--interactive', action='store_true',
                      help='Run interactive chat')
  
  config_p = subparsers.add_parser('ls', help='List resources')
  config_p.add_argument('resource', type=str, 
                      help='For now only models')
  config_p.set_defaults(func=main_ls)


  try:
    args = parser.parse_args()

    if not os.path.exists(args.logdir):
      os.makedirs(args.logdir)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)

    fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", str(uuid.uuid4())))
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    args.func(args)
  except Exception as e:
    parser.print_help()
    raise


if __name__ == "__main__":  
  main()