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
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Чтобы запустить игру, напишите "start"'
        sessionStorage[user_id] = {'started': False, 'hidden_word': False}
        return

    if not sessionStorage[user_id]['started']:
        is_started = req['request']['original_utterance'] == 'start'
        if is_started:
            sessionStorage[user_id]['started'] = True
            if not sessionStorage[user_id]['hidden_word']:
                sessionStorage[user_id]['hidden_word'] = choice(open('words.txt').readline().split())
            res['response']['text'] = 'Напишите букву'
