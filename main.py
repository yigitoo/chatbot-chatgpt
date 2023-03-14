from uuid import uuid4 as gen_uid
from dotenv import load_dotenv as load_config
import openai
import os
import flet as ft

load_config()
openai.api_key = os.getenv('API_KEY')


def api_request(question: str, model: str = "gpt-3.5-turbo") -> dict:
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user",
                   "content": question}]
    )

    answer_of_question = response.choices[0].message.content 

    return answer_of_question




def main(page: ft.Page):
    page.scroll = "auto"
    allmessages = ft.Column(scroll="auto")

    def sendmessage(e):
        try:
            # AND IF SUCCESS SEND YOU CALL PUBSUB
            # FOR SEND YOU FRIEND ON REALTIME MESSAGE
            # LIKE WEBSOCKET
            if txtchat.value != "":
                page.pubsub.send_all(f"{username.value}:{txtchat.value}")
                make_request_to_chatbot(question = txtchat.value)
                # CLEAR INPUT MESSAGE
                txtchat.value = ""
                page.update()
        except Exception as e:
            print(e)
            print("MESSAGE FAILED TO SEND")

    # NOW CREATE PUBSUB FUNCTION FOR RECEIVE MESSAGE FROM YOU FRIEND

    def on_message(msg):
        # NOW REMOVE :
        # EXAMPLE jaja:lili
        # I WANT GET jaja value from statement above
        split_msg = msg.split(":")
        allmessages.controls.append(
            ft.Row([
                ft.Container(
                    padding=20,
                    border_radius=30,
                    # THIS SCRIPT IS IF YOU SENDER THEN COLOR BLUE
                    bgcolor="blue200" if split_msg[0] == username.value else "orange200",
                    content=ft.Column([
                            ft.Text(split_msg[0]),
                            ft.Text(split_msg[1],
                                    size=22,
                                    weight="bold"
                                    ),

                    ])

                )

                # NOW IF YOU SENDER THEN YOU CONTAINER ALIGN RIGHT OR RECEIVE THEN COINTAINER ALIGN LEFT

            ], alignment="end" if split_msg[0] == username.value else "start")
        )
        page.update()

    page.pubsub.subscribe(on_message)

    # NOW CREATE getmessage IF YOU FLET APP FIRST LOADED
    # THEN GET DATA FROM FIRESTORE THEN PUSH TO WIDGET

    def getmessage(e):
        page.dialog.open = False
        if username.value == "":
            return
        allmessages.controls.append(
            ft.Row([
                ft.Container(
                    padding=20,
                    border_radius=20,
                    # THIS SCRIPT IS IF YOU SENDER THEN COTNAINER COLOR IS BLUE
                    bgcolor="blue200",
                    content=ft.Column([
                        ft.Text(f"{username.value}"),
                        ft.Text(f"Hello, I'm {username.value}!",
                                size=22,
                                weight="bold"
                                ),

                    ])
                )

            ], alignment="end")
        )

        username.visible = False
        page_layout.visible = True
        page.update()

    # CREATE NAME OF YOU CHAT
    page.dialog = ft.AlertDialog(
        open=True,
        modal=True,
        title=ft.Text("Welcome!"),
        content=ft.Column([username := ft.TextField(label="Give your username")], tight=True),
        actions=[ft.ElevatedButton(text="Join chat", on_click=getmessage)],
        actions_alignment="end",
    )
    # CREATE TEXTFIELD FOR CHAT MESSAGE
    txtchat = ft.TextField(label="message",
                           # REMOVE BORDER
                           border=ft.InputBorder.OUTLINE,
                           text_size=20,
                           on_submit=sendmessage,
                           expand=True
                           )

    # CREATE CONTAINER FOR TEXTFIELD MESSAGE AND BUTTON SEND
    chat_contianer = ft.Container(
        bgcolor="blue",
        padding=20,
        border_radius=30,
        content=ft.Row([
            txtchat,
            ft.IconButton(icon="send",
                          icon_size=30,
                          on_click=sendmessage
                          )

        ])

    )

    # NOW CREATE LAYOUT FOR ALL CHAT AND YOU TEXTFIELD MESSAGE
    page_layout = ft.Column([
        ft.Container(
            height=500,
            content=ft.Column([
                allmessages,
            ], scroll="auto")
        ),
        chat_contianer
    ])

    # AND SET DEFAULT TEXTFIELD FOR SEND MESSAGE IS HIDE
    page_layout.visible = False

    page.add(
        ft.Column([
            ft.Row([
                ft.Text("CHATBOT WITH CHATGPT AND WHISPER", size=30,
                        weight="bold",
                        text_align=ft.TextAlign.CENTER
                        ),
                username
            ]),
            page_layout
        ], alignment="end")
    )

    def make_request_to_chatbot(question: str) -> str :
        response = api_request(question)
        
        allmessages.controls.append(
            ft.Row([
                ft.Container(
                    padding=20,
                    border_radius=20,
                    # THIS SCRIPT IS IF YOU SENDER THEN COTNAINER COLOR IS BLUE
                    bgcolor="green200",
                    content=ft.Column([
                        ft.Text(f"ChatGPT"),
                        ft.Text(f"{response.choices[0].message.content}",
                                size=22,
                                weight="bold"
                                ),

                    ])
                )

            ], alignment="start")
        )
ft.app(target=main)
