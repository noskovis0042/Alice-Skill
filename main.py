from random import choice
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}


@app.route('/post', methods=['POST'])
def skill():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Request: %r', response)
    return jsonify(response)


def handle_dialog(res, req):
    def get_state():
        return '\n'.join([f"Неотгаданные буквы: {', '.join(sessionStorage[user_id]['hidden_letters'])}",
                          f"Отгаданные буквы: {', '.join(sessionStorage[user_id]['guessed_letters'])}",
                          "Напишите букву"])

    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Чтобы запустить игру, напишите "start"'
        sessionStorage[user_id] = {'started': False, 'hidden_word': False,
                                   'hidden_letters': list('АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'), 'guessed_letters': []}
        return

    if not sessionStorage[user_id]['started']:
        is_started = req['request']['original_utterance'] == 'start'
        if is_started:
            sessionStorage[user_id]['started'] = True
            if not sessionStorage[user_id]['hidden_word']:
                sessionStorage[user_id]['hidden_word'] = choice(open('data/words.txt').readline().split())
            res['response']['text'] = get_state()


if __name__ == '__main__':
    app.run()
