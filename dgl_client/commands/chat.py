import typer
import logging
from ..api_cli import APIClient, InferenceClient
from .utils import get_inf_client, do_login, DGL_API_ENDPOINT

logger = logging.getLogger(__name__)
app = typer.Typer()

@app.callback(invoke_without_command=True)
def send_message(
    msg:str ,
    model: str,
    chat_id: str = "",
    interactive: bool = False,
    collection: str = "",
    endpoint: str = typer.Option(default=DGL_API_ENDPOINT),
    inference_url: str = typer.Option(default="inference"),
    access_key: str = ""
):
    """
    Send a message MSG to a MODEL

    Use --interactive to enter in a conversation loop with the agent
    Use --collection <CID> to add documents in the collection to the context of the chat

    Use --endpoint http(s)://URL:PORT to set the base endpoint url for the service
    Use --inference-url to add to the base endpoint url in case the server is not on /

    Use --access-key <TOKEN> to set the TOKEN for authorized API access

    """
    client = get_inf_client(endpoint, inference_url)

    do_login(access_key, client)

    if chat_id:
        chat_id = client.continue_chat(chat_id)
    else:
        chat_id = client.create_chat()

    logger.info(f"Chat ID: {chat_id}")

    events = client.send_message(msg, model, collection=collection)

    print()
    print("You: %s"%(msg))
    print()
    print("Assistant: ", end="", flush=True)
    ass_reply = []
    for event in events:
        print(event, end="", flush=True)
        ass_reply.append(event)
    print()
    return ass_reply


if __name__ == "__main__":
    app()
