from random import choice
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}
difficulties = range(5, 18 + 1)


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
        res['response']['text'] = 'Чтобы запустить игру, напишите "start [количество букв]"'
        sessionStorage[user_id] = {'started': False, 'hidden_word': False, 'difficulty': 0,
                                   'hidden_letters': list('АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'),
                                   'guessed_letters': []}
        return

    if not sessionStorage[user_id]['started']:
        is_started = req['request']['original_utterance'][:5] == 'start'
        sessionStorage[user_id]['difficulty'] = int(req['request']['original_utterance'][6:])
        if is_started:
            if sessionStorage[user_id]['difficulty'] in difficulties:
                sessionStorage[user_id]['started'] = True
                sessionStorage[user_id]['difficulty'] = int(req['request']['original_utterance'][6:])
                if not sessionStorage[user_id]['hidden_word']:
                    sessionStorage[user_id]['hidden_word'] = choice(
                        [word for word in open('data/words.txt').readline().split() if
                         len(word) == sessionStorage[user_id]['difficulty']])
                res['response']['text'] = get_state()
            else:
                res['response']['text'] = 'Увы, у нас нет слов с таким количеством букв'


if __name__ == '__main__':
    app.run()
