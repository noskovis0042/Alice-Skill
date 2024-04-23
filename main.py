from random import choice
from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}
difficulties = range(5, 18 + 1)
letters = list('АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')


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
        cur_word = []
        for letter in sessionStorage[user_id]['hidden_word']:
            if letter in sessionStorage[user_id]['guessed_letters']:
                cur_word.append(letter)
            else:
                cur_word.append('_')
        return '\n'.join(["Слово: " + "".join(cur_word),
                          f"Неотгаданные буквы: {', '.join(sessionStorage[user_id]['hidden_letters'])}",
                          f"Отгаданные буквы: {', '.join(sessionStorage[user_id]['guessed_letters'])}",
                          "Напишите букву"])

    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Чтобы запустить игру, напишите "start [количество букв]"'
        sessionStorage[user_id] = {'started': False, 'hidden_word': False, 'difficulty': 0,
                                   'hidden_letters': letters,
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
                    words = [word for word in open('data/words.txt', encoding='utf-8').readline().split() if
                             len(word) == sessionStorage[user_id]['difficulty']]
                    sessionStorage[user_id]['hidden_word'] = choice(words).upper()
                res['response']['text'] = get_state()
            else:
                res['response']['text'] = 'Увы, у нас нет слов с таким количеством букв'
    else:
        inp = req['request']['original_utterance']
        ret = ""
        if inp in letters:
            if inp in sessionStorage[user_id]['hidden_letters']:
                sessionStorage[user_id]['guessed_letters'].append(
                    sessionStorage[user_id]['hidden_letters'].pop(sessionStorage[user_id]['hidden_letters'].index(inp)))
            else:
                ret = "Вы уже называли эту букву. Попробуйте другую."
        else:
            ret = "Неправильный ввод."

        if all([(letter in sessionStorage[user_id]['guessed_letters']) for letter in
                sessionStorage[user_id]['hidden_word']]):
            res['response'][
                'text'] = f"Вы отгадали все буквы слова!\nЗагаданное слово: {sessionStorage[user_id]['hidden_word']}"
            return

        res['response']['text'] = ret + "\n" + get_state()


if __name__ == '__main__':
    app.run()
