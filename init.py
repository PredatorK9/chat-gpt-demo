import openai

def initialise_key():
    """
    Initialise the api key to make requests to OpenAI server.
    """
    openai.api_key = open("./openai_api_key.txt", "r").read().split('\n')[1].strip()
    