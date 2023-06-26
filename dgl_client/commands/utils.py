import os
from loguru import logger

from ..api_cli import APIClient, InferenceClient, BackendClient


DGL_INF_ENDPOINT = "https://www.diglife.eu/"
if "DGL_INF_ENDPOINT" in os.environ and os.environ["DGL_INF_ENDPOINT"]:
    DGL_INF_ENDPOINT = os.environ["DGL_INF_ENDPOINT"]

DGL_BCK_ENDPOINT = "https://www.diglife.eu/"
if "DGL_BCK_ENDPOINT" in os.environ and os.environ["DGL_BCK_ENDPOINT"]:
    DGL_BCK_ENDPOINT = os.environ["DGL_BCK_ENDPOINT"]    

def get_inf_client(endpoint: str = DGL_INF_ENDPOINT, url: str="inference", debug=False) -> InferenceClient:
  if url: endpoint = os.path.join(endpoint, url)
  logger.info("Connecting to API Endpoint %s"%endpoint)
  client = InferenceClient(backend_url=endpoint, debug=debug)    
  return client

def get_back_client(endpoint: str = DGL_INF_ENDPOINT, url: str = "api/v1", debug=False) -> BackendClient:
  if url: endpoint = os.path.join(endpoint, url)
  logger.info("Connecting to API Endpoint %s"%endpoint)
  client = BackendClient(backend_url=endpoint, debug=debug)    
  return client

def do_login(access_key, client):
  if access_key:
    return client.login(access_key)
  return False  