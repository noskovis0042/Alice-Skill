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

        sessionStorage[user_id] = {
            'started': None
        }
        return

    if sessionStorage[user_id]['started'] is None:
        pass
