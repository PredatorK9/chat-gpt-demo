import gradio as gr
from chat_completion import send_message
from init import initialise_key
from utils import append_user_prompt

MESSAGE_HISTORY = []
CONTEXT = ""


def run():
    with gr.Blocks() as demo:
        chatbot_ui = gr.Chatbot().style(height=640)
        context_field = gr.Textbox(
            label="Context for the chat",
            show_label="True", 
            placeholder= "If you want to have a chat with some context in mind.\nPress \"Enter to save the context first!\"",
            )
        msg_field = gr.Textbox(label="Message", show_label=True, placeholder="Enter prompt")
        clear_button = gr.Button("Clear")

        context_field.submit(set_context_for_chat, context_field, context_field)
        msg_field.submit(respond, [msg_field, chatbot_ui], [msg_field, chatbot_ui])
        clear_button.click(lambda: MESSAGE_HISTORY.clear(), None, chatbot_ui, queue=False)

    demo.launch(share=False)


def set_context_for_chat(context_prompt):
    global CONTEXT
    global context_placeholder_string
    CONTEXT = context_prompt
    context_placeholder_string = f"Context set to {context_prompt}"
    return context_prompt


def respond(user_prompt, chat_history):
    global MESSAGE_HISTORY
    global CONTEXT

    if CONTEXT != "":
        MESSAGE_HISTORY = append_user_prompt(":".join([CONTEXT, user_prompt]), MESSAGE_HISTORY)
    else:
        MESSAGE_HISTORY = append_user_prompt(user_prompt, MESSAGE_HISTORY)

    model_response, MESSAGE_HISTORY = send_message(MESSAGE_HISTORY)
    chat_history.append((user_prompt, model_response))
    return "", chat_history


def main():
    initialise_key()
    run()


if __name__ == "__main__":
    main()
