from dotenv import load_dotenv as load_config
import openai
import os
import flet as ft
from typing import Union


openai.api_key = os.environ['API_KEY']

def make_question(question: str, model: str = "gpt-3.5-turbo") -> dict:
    completion = openai.ChatCompletion.create(
        model = model,
        messages = [{"role": "user",
                     "content": question}]
    )
    return completion


class Gui:
    global page, chat, new_message
    
    @staticmethod
    def main(page: ft.Page):
        
        chat = ft.Column()
        new_message = ft.TextField()

        page.add(
            chat, ft.Row(controls=[new_message, ft.ElevatedButton("Send", on_click=Gui.send_click)])
        )

    @staticmethod
    def send_click(e):
        chat.controls.append(ft.Text(new_message.value))
        new_message.value = ""
        page.update()

if __name__ == "__main":
    ft.app("chatbot-with-chatgpt-and-whisper", target=Gui.main, view=ft.WEB_BROWSER)