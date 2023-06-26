import json
import os
from base64 import b64decode, b64encode
import requests
from loguru import logger

def inf_prepare_token(api_key: str, user_id: str , provider_account_id: str, username: str, client="website"):
    token_data = {
        "api_key": api_key,
        "client": client,
        "user_id": user_id,
        "provider_account_id": provider_account_id,
        "username": username
    }

    token = b64encode(json.dumps(token_data).encode())
    return token


def inf_login_check(endp, tok):
    logger.info("Trying to login...")
    username = None
    try:
      response = requests.get(
          f"{endp}/auth/check",
          json={},
          headers={"Authorization": f"Bearer {tok}"},
      )
      response.raise_for_status()
      username = response.json()
    except:
      pass

    return username

def inf_refresh_token(endp, atok, rtok):
    logger.info("Refreshing login token...")
    new_tok = None
    try:
      response = requests.get(
          f"{endp}/auth/refresh",
          json={},
          headers={
              "Refresh": f"{rtok}"
              },
      )
      response.raise_for_status()
      new_tok = response.json()
    except:
      raise
    logger.debug("New token is %s"%str(new_tok))

    return new_tok

def inf_ak2token(endp, access_key):
    logger.info("Logging in using access_key...")
    new_tok = None
    try:
      response = requests.post(
          f"{endp}/auth/trusted_login",
          json={},
          headers={
              "TrustedClient": f"{access_key}"
              },
      )
      response.raise_for_status()
      new_tok = response.json()
    except:
      raise
    logger.debug("New token is %s"%str(new_tok))

    return new_tok

def bck_ak2token(endp, access_key):
    logger.info("Logging in using access_key...")
    new_tok = None
    try:
      response = requests.post(
          f"{endp}/admin/api_client",
          json={},
          headers={
              "TrustedClient": f"{access_key}"
              },
      )
      response.raise_for_status()
      new_tok = response.json()
    except:
      raise
    logger.debug("New token is %s"%str(new_tok))

    return new_tok    

def bck_login_check(endp, access_key):
    logger.info("Trying to login...")
    username = None
    try:
      response = requests.get(
          os.path.join(endp, 
            f"auth/check_client"
            ),
          json={},
          headers={"X-API-Key": f"{access_key}"},
      )
      response.raise_for_status()
      username = response.json()
    except Exception as e:
      logger.error(f"Login failed with error {e}")


    return username    

