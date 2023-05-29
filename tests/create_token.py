import argparse
import requests
import json
import os
from dgl_client.api_cli import prepare_token
import uuid

def main(args):

  token = prepare_token(
    username=args.username,
    api_key=args.access_key,
    user_id=args.user_id,
    provider_account_id=args.provider,
  )

  return token

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='New user client.')
  parser.add_argument('-u','--username', type=str,required=True,
                      help='User for which to create the API')
  parser.add_argument('-k','--access_key', type=str,default=str(uuid.uuid4()),
                      help='Access key')  
  parser.add_argument('-i','--user_id', type=str,required=True,
                      help='User id')    
  parser.add_argument('-p','--provider', type=str,default="SDK",
                      help='Provider')      

  args = parser.parse_args()
  print(args)
  
  token = main(args)

  print("Token", token)

