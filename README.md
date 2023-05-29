# Diglife API client

Run `pip install dgl_client` to install the package. 

Available commands:
* dglc ls models #This returns a list of all the available models, so that you know which one to use in the chat command
* dglc chat #This create a new chat with one of the assistants. You will need an API_KEY for that 

You will need an API_KEY in order to interact with the assistants, please contact JRC.F7 with your work email to obtain one.

e.g.
~~~
$ dglc ls models
2023-05-29 13:39:47,874 [INFO ] - [main.py > get_client() > 15] Connecting to API Endpoint https://www.diglife.eu/inference
2023-05-29 13:39:48,257 [INFO ] - [main.py > list_models() > 22] Available models ['OA_SFT_Pythia_12B', 'JRC_RHLF_13B', 'OA_GPT3']
2023-05-29 13:39:48,496 [INFO ] - [main.py > list_models() > 25] Available workflows ['vAST_GPT3.5']
~~~

~~~
$ dglc chat -m OA_SFT_Pythia_12B -k $DGL_TOK "Who are you?"
2023-05-29 13:40:15,466 [INFO ] - [main.py > get_client() > 15] Connecting to API Endpoint https://www.diglife.eu/inference
2023-05-29 13:40:15,466 [INFO ] - [api_cli.py > ak2token() > 63] Logging in using access_key...
2023-05-29 13:40:15,720 [INFO ] - [api_cli.py > login_check() > 28] Trying to login...
2023-05-29 13:40:15,966 [INFO ] - [api_cli.py > login() > 96] Logged in as [redacted]
2023-05-29 13:40:16,195 [INFO ] - [main.py > main_chat() > 61] Chat ID: [redacted]

You: Who are you?

Assistant: I am Open Assistant, an open source chat-based virtual assistant. I was trained by volunteers to answer questions and provide information on a wide range of topics. How can I help you today?
~~~


