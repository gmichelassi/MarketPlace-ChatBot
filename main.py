import os
import uuid
import json

from dotenv import load_dotenv
from subprocess import call
from ChatBot import ChatBot

load_dotenv()


def format_assistant_text(text: str) -> str:
    return f"\033[1;32mAssistente:\033[0m {text}"


def clear():
    _ = call('clear' if os.name == 'posix' else 'cls')


if __name__ == '__main__':
    bot = ChatBot()
    session_id = str(uuid.uuid4())

    clear()

    print(f"\033[3mIniciando conversa com o ID: {session_id}\033[0m")
    print(format_assistant_text('Olá! Como posso te ajudar?'))

    while True:
        user_input = input(f"\033[1;34mVocê:\033[0m ")

        response = bot.ask(session_id=session_id, message=user_input)

        try:
            response = json.loads(response)
            if response.get('end_conversation'):
                print(format_assistant_text('Obrigado pela conversa, espero que tenha conseguido te ajudar, até mais!'))
                quit()
            elif response.get('restart_conversation'):
                session_id = str(uuid.uuid4())
                clear()

                print(f"\033[3mIniciando conversa com o ID: {session_id}\033[0m")
                print(format_assistant_text('Olá! Como posso te ajudar?'))
                continue
        except ValueError:
            print(format_assistant_text(response))
