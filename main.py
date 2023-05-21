import argparse
import logging
import os
from api_cli import APIClient
import uuid

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

def main_config(args):
  match args.command:
    case "ls-models":
      list_models(args)

def main_chat(args):
  client = get_client(args)

  model_config_name = args.model

  client.login(args.login)
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


if __name__ == "__main__":
  API_ENDPOINT = "https://www.diglife.eu/inference"

  parser = argparse.ArgumentParser(description='DigLige API Client.')
  parser.add_argument('--logdir', type=str, default="logs/",
                      help='Where to store logs')
  parser.add_argument('--endpoint', type=str, default=API_ENDPOINT,
                      help='Endpoint for the inference')

  subparsers = parser.add_subparsers(help='You can choose between different commands')
  chat_p = subparsers.add_parser('chat', help='chat with the assistants')
  chat_p.set_defaults(func=main_chat)

  chat_p.add_argument('message', type=str, 
                      help='say something to the model')
  chat_p.add_argument('-c','--chat-id', type=str,
                      help='Continue previous chat')
  chat_p.add_argument('-l','--login', type=str, required=True,
                      help='Access key to authenticate to the API')
  chat_p.add_argument('-m','--model', type=str, required=True,
                      help='Which model do you want to talk to?')
  chat_p.add_argument('-i','--interactive', action='store_true',
                      help='Run interactive chat')
  
  
  config_p = subparsers.add_parser('config', help='check configuration')
  config_p.add_argument('command', type=str, 
                      help='Select command')
  config_p.set_defaults(func=main_config)

  args = parser.parse_args()
  print(args)

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