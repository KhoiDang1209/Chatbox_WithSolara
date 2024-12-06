import solara
from solara.tasks import use_task
import solara.lab as lab
from langchain_ollama.llms  import OllamaLLM
manager=solara.reactive([])

@solara.component
def get_ai_chat(chain: OllamaLLM, current_message:str):
    ai_mess=chain.invoke(current_message)
    manager.set(manager.get()+[{'user': current_message,'ai':ai_mess}])
    return lab.ChatMessage(children=[solara.Markdown(md_text= ai_mess)],user=False)


@solara.component
def show_chat(
    mess_reactive: solara.Reactive,
    config_model=dict,
    list_message_user_reactive: solara.Reactive=None,
    list_message_chatbox_reactive: solara.Reactive=None,

):
    chain=config_model['prompt']|config_model['model']
    if mess_reactive.value != '':
        with lab.ChatBox() as chat_box:
            user_chat_mess=lab.ChatMessage(children=[mess_reactive.value],user=True)
        get_ai_chat_response=use_task(lambda chain=chain,current_mess=mess_reactive.value:get_ai_chat(chain,current_mess),dependencies=[chain,mess_reactive.value])
        if get_ai_chat_response.finished:
            with lab.ChatBox() as chat_box:
                for mess in manager.get():
                    user_chat_mess=lab.ChatMessage(children=[
                        solara.Markdown(md_text=mess['user']),
                    ],user=True)
                    ai_chat_mess=lab.ChatMessage(children=[
                        solara.Markdown(md_text=mess['ai'])
                    ],user=False)
            return chat_box
        solara.ProgressLinear(value=get_ai_chat_response.progress,)


