import os
import logging
from ..api_cli import APIClient, InferenceClient, BackendClient

logger = logging.getLogger(__name__)

DGL_INF_ENDPOINT = "https://www.diglife.eu/"
if "DGL_INF_ENDPOINT" in os.environ and os.environ["DGL_INF_ENDPOINT"]:
    DGL_INF_ENDPOINT = os.environ["DGL_INF_ENDPOINT"]

DGL_BCK_ENDPOINT = "https://www.diglife.eu/"
if "DGL_BCK_ENDPOINT" in os.environ and os.environ["DGL_BCK_ENDPOINT"]:
    DGL_BCK_ENDPOINT = os.environ["DGL_BCK_ENDPOINT"]    

def get_inf_client(endpoint: str, inference_url: str) -> InferenceClient:
  logger.info("Connecting to API Endpoint %s"%endpoint)
  client = APIClient(endpoint, inf_url=inference_url)    
  return client._inference

def get_back_client(endpoint: str, inference_url: str) -> BackendClient:
  logger.info("Connecting to API Endpoint %s"%endpoint)
  client = APIClient(endpoint, inf_url=inference_url)    
  return client._backend

def do_login(access_key, client):
  if access_key:
    return client.login(access_key)
  return False  