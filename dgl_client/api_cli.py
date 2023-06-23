import time
import os
import logging
import json
import requests
import sseclient
import uuid
from rich import print

logger = logging.getLogger(__name__)

from .utils import inf_ak2token, inf_login_check, inf_prepare_token, inf_refresh_token
from .utils import bck_ak2token, bck_login_check

# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1

class BaseClient:
    
    def __init__(self, backend_url, http_client=requests):
        self.backend_url = backend_url
        self.http_client = http_client
        self.auth_headers = None

class BackendClient(BaseClient):
    def login(self, access_key) -> str|None:
        logger.info(f"Trying to login with {access_key}")    

        #atok = bck_ak2token(self.backend_url, access_key)
        username = bck_login_check(self.backend_url, access_key)

        if username:
            logger.info(f"Logged in as {username}")    
            self.auth_headers = {"X-API-Key": f"{access_key}"}    
        return username


    def create_collection(self, 
            name:str , 
            descr:str, 
            bucket:str|None = None
        ) -> str:
        bucket = bucket if bucket != None else name
        response = requests.post(
            f"{self.backend_url}/data/create_collection/",
            params={
                "collection_name":name,
                "collection_descr":descr,
                "collection_bucket":bucket
            },
            headers=self.auth_headers,
        )
        response.raise_for_status()
        return response.json()        

    def upload_document(self, cid, path:str) -> str:
        with open(path,'rb') as fp:
            response = requests.post(
                f"{self.backend_url}/data/collections/{cid}/upload",
                files=[
                    ("files", (path, fp)),
                ],
                headers=self.auth_headers
            )

        response.raise_for_status()
        return response.json()  

    def upload_documents(self, cid:str, paths:list[str]) -> list[str]:
        ids = []
        for path in paths:
            ids.append(
                self.upload_document(cid, path)
            )
        return ids
                 
         

    def get_collections(self) -> str:
        response = requests.get(
            f"{self.backend_url}/data/collections/",
            json={},
            headers=self.auth_headers,
        )
        response.raise_for_status()
        return response.json()

    def list_settings(self):        
        response = requests.get(
            f"{self.backend_url}/admin/backend_settings/public",
            json={},
            headers=self.auth_headers,
        )
        response.raise_for_status()
        print(response.json())
class InferenceClient(BaseClient):

    def login(self, access_key):
        atok = inf_ak2token(self.backend_url, access_key)
        username = inf_login_check(self.backend_url, atok)
        if username:
            logger.info(f"Logged in as {username}")    
            self.auth_headers = {"Authorization": f"Bearer {atok}"}
        
        return username

    def continue_chat(self, chat_id, message_id=None):
        self.chat_id = chat_id
        if not message_id:
            mess = self.list_messages(chat_id)
            if len(mess) > 0:
                message_id = mess[0]
        self.message_id = message_id
        return self.chat_id

    def create_chat(self):
        response = self.http_client.post(
            f"{self.backend_url}/chats",
            json={},
            headers=self.auth_headers,
        )
        response.raise_for_status()
        self.chat_id = response.json()["id"]
        self.message_id = None
        return self.chat_id

    def list_chats(self):
        response = self.http_client.get(
            f"{self.backend_url}/chats",
            json={},
            headers=self.auth_headers,
        )
        response.raise_for_status()
        res = response.json()

        bag = []
        if "chats" in res:
            for chat in res["chats"]:
                bag.append((chat["id"], chat["title"]))

        return bag

    def list_messages(self, chat_id):
        response = self.http_client.get(
            f"{self.backend_url}/chats/%s"%chat_id,
            json={},
            headers=self.auth_headers,
        )
        response.raise_for_status()
        res = response.json()
        messages = res["messages"]
        bag = []
        for message in messages:
            bag.append(message["id"])
        return bag        

    def get_available_models(self):
        response = self.http_client.get(
            f"{self.backend_url}/configs/model_configs",
            headers=self.auth_headers,
        )
        response.raise_for_status()
        return [model["name"] for model in response.json()]
    
    def get_available_workflows(self):
        response = self.http_client.get(
            f"{self.backend_url}/configs/workflow_configs",
            headers=self.auth_headers,
        )
        response.raise_for_status()
        return [model["name"] for model in response.json()]

    def embed(self, message):
        model_id=""
        response = self.http_client.post(
            f"{self.backend_url}/embed",
            json={
                "input": message,
                "model": model_id,
            },
            headers=self.auth_headers,
        )
        response.raise_for_status()
        embed = response.json()['data'][0]['embedding']
        print("EMBED",embed)
        return embed
        

    def send_message(self, message, model_config_name, collection=None):
        print("PARENT:",self.message_id)
        response = self.http_client.post(
            f"{self.backend_url}/chats/{self.chat_id}/prompter_message",
            json={
                "parent_id": self.message_id,
                "content": message,
                "data": {"collection": collection}
            },
            headers=self.auth_headers,
        )
        response.raise_for_status()
        prompter_message_id = response.json()["id"]
        print("MESSAGEID",prompter_message_id)

        response = self.http_client.post(
            f"{self.backend_url}/chats/{self.chat_id}/assistant_message",
            json={
                "parent_id": prompter_message_id,
                "model_config_name": model_config_name,
                "sampling_parameters": {
                    "top_p": 0.95,
                    "top_k": 50,
                    "repetition_penalty": 1.2,
                    "temperature": 1.0,
                },
            },
            headers=self.auth_headers,
        )
        response.raise_for_status()
        self.message_id = response.json()["id"]

        response = self.http_client.get(
            f"{self.backend_url}/chats/{self.chat_id}/messages/{self.message_id}/events",
            stream=True,
            headers={
                "Accept": "text/event-stream",
                **self.auth_headers,
            },
        )
        response.raise_for_status()
        if response.status_code == 204:
            response = self.http_client.get(
                f"{self.backend_url}/chats/{self.chat_id}/messages/{self.message_id}",
                headers=self.auth_headers,
            )
            response.raise_for_status()
            data = response.json()
            yield data["content"]
        else:
            client = sseclient.SSEClient(response)
            events = iter(client.events())
            for event in events:
                if event.event == "error":
                    raise RuntimeError(event.data)
                if event.event == "ping":
                    continue
                try:
                    data = json.loads(event.data)
                except json.JSONDecodeError:
                    raise RuntimeError(f"Failed to decode {event.data=}")
                event_type = data["event_type"]
                if event_type == "token":
                    yield data["text"]
                elif event_type == "message":
                    # full message content, can be ignored here
                    if "message" in data:
                        if "content" in data['message']:
                            yield data['message']["content"]
                        else:
                            _s = data["message"]
                            logger.debug(f"Message event type but no content? {_s=}")                             
                    else:
                        logger.debug(f"Message event type but no message? {data=}")    
                elif event_type == "error":
                    raise RuntimeError(data["error"])
                elif event_type == "pending":
                    logger.debug(f"Message pending. {data=}")
                else:
                    print("Received unknown event_type!!!")
                    print(data)
    

class APIClient:
    def __init__(self, base_url, api_url="/api/v1", inf_url="/inference", http_client=requests):
        backend_url = base_url + api_url
        self._backend = BackendClient(backend_url)

        inference_url = base_url + inf_url
        self._inference = InferenceClient(inference_url)

    def login(self, access_key):
        self._backend.login(access_key)
        self._inference.login(access_key)        


        





