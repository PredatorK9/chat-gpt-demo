import openai
from utils import num_tokens_from_messages, token_usage_check
import os


def send_message(messages, model='gpt-3.5-turbo-0301', token_limit=4096):
    """
    A function which is used for sending messages to given model at OpenAI servers.
    \n This implementation for now only accepts `model` to be `gpt-3.5-turbo-0301`.
    \n`token_limit` is to define the limit of tokens to avoid wastage of api calls once the limit has been exceeded.
    The default value is set to `4096` which is the limit for the model `gpt-3.5-turbo-0301`.
    """
    # num_tokens = num_tokens_from_messages(messages, model)  # getting the number of tokens being used
    # token_usage_check(num_tokens, token_limit) # checking the token usage before making API call

    completion = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )

    model_response = completion["choices"][0]["message"]["content"]   # extracting the text returned by model from the JSON
    messages.append({"role" : completion["choices"][0]["message"]["role"], "content": completion["choices"][0]["message"]["content"]}) # appening the response returned by the model to message history
    print(*messages[-2:])

    return model_response, messages
    