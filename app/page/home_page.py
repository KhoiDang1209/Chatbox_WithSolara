import solara
import solara.lab as lab
from app.component import show_chat
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms  import OllamaLLM
import streamlit as st

template="""Question:{question}
 Answer: {answer}"""
prompt=ChatPromptTemplate.from_template(template)

model=OllamaLLM(model='llama3.1')



message=solara.reactive('')
list_message_user=solara.reactive([])
list_message_chatbox=solara.reactive([])

def send_message(mes: str):
    message.set(mes)
    list_message_user.set(list_message_user.get() + [mes])
    print(message.value,list_message_user.value)


@solara.component
def home_page():
    with solara.Div(
        style={
            'height': '100vh',
        }
    ) as container:
        with solara.Div(
            style={
                'height': '70%',
                'border-bottom': '1px solid #ccc',
                'border-radius': '5px',
                'shadow': '0 0 10px rgba(0,0,0,0.1)',
                'overflow-y': 'auto',
            }
        ) as showchat:
            show_chat(
                mess_reactive=message,
                config_model={
                    'model': model,
                    'prompt': prompt,
                }
            )
        with solara.Div(
            style={
                'padding': '5px',
            }
        ) as chat_box:
            lab.ChatInput(send_callback=send_message)



