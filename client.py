import asyncio
import flet as ft
from websockets.asyncio.client import connect
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK


async def main(page: ft.Page):
    page.window.width = 400
    username_ref = ft.Ref[ft.TextField]()
    message_ref = ft.Ref[ft.TextField]()
    messages_ref = ft.Ref[ft.ListView]()
    websocket = await connect('ws://localhost:8999')

    async def send_message(e):
        message = f'{username_ref.current.value}: {message_ref.current.value}'
        await websocket.send(message)  # type: ignore
        message_ref.current.value = ""
        message_ref.current.update()        
    
    async def check_messages():
        while True:
            try:
                message = await websocket.recv() 
                messages_ref.current.controls.append(ft.Text(message, color='black'))  # type: ignore
                messages_ref.current.update()
            except (ConnectionClosedError, ConnectionClosedOK) as e:
                messages_ref.current.controls = [
                    ft.Text(f'Conexão fechada inesperadamente: {str(e)}', color='red')
                ]
    
    asyncio.create_task(check_messages())

    async def go_chat(e):
        chat = ft.Column([
            ft.Container(
                ft.ListView(
                    [
                        ft.Text('Chat', color='black')
                    ],
                    height=200,
                    ref=messages_ref
                ),
                bgcolor=ft.colors.GREY_100
            )
        ])
        message = ft.TextField(label='Digite sua mensagem', ref=message_ref)
        submit = ft.IconButton(ft.icons.SEND, on_click=send_message)

        page.controls = [chat, message, submit]
        page.update()

    p1 = ft.Column([
            ft.TextField(label='username', ref=username_ref),
            ft.IconButton(ft.icons.NAVIGATE_NEXT, on_click=go_chat)
    ])

    page.add(p1)


if __name__ == '__main__':
    ft.app(main)
