import tiktoken


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """
    Returns the number of tokens used by a list of message for a
    particular model.
    Default model is set to `gpt-3.5-turbo-0301`.
    """
    num_tokens = 0
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("warning: Model not found. Using cl100k_base encoding\n")
    if model == "gpt-3.5-turbo-0301":
        # every message follows </start/>{role/name}\n{context}</end>\n
        tokens_per_message = 4
        tokens_per_name = -1        # if there is a name, the role is omitted
    else:
        raise NotImplementedError(
            f"num_tokens_from_messages() is not implemented for model {model}")

    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name

    num_tokens += 3                 # every reply is primed with </start>assistant</end>
    return num_tokens


def token_usage_check(num_tokens, token_limit):
    # if the token limit is exceeded then terminate the application
    # TODO: Add a feature for user to be able to restart the session rather than
    # running the script again.
    if num_tokens > token_limit:
        print("========= Token limit exceeded ========")
        exit()

    # if the token is at 80% of the limit then give user a warning
    if num_tokens >= 0.8 * token_limit:
        print("Warning: Token usage is at 80% \n")


def append_user_prompt(prompt, history):
    history.append({
        "role": "user",
        "content": prompt
    })
    return history
