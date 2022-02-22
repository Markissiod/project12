import json

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
# Главная страница, В зависимости от settings выводит если приложение работает или нет
def index():
    with open('settings.json') as file:
        settings = json.load(file)
    return render_template('index.html', **settings)


@app.route('/candidate/<id>')
# Выводим данные об кандидатов
def candidates(id):
    with open('candidates.json', encoding='utf-8') as file:
        candidates_ = json.load(file)
    for candidate in candidates_:
        if candidate['id'] == int(id):
            return render_template('candidate.html', **candidate)


@app.route('/list/')
# Выводим список всех кандидатов
def name_list():
    with open('candidates.json', encoding='utf-8') as file:
        candidates_ = json.load(file)
        return render_template('list_name.html', user=candidates_)


@app.route('/search/')
# Поиск по совпадению.
def search_name():
    name = request.args.get("name")
    with open('candidates.json') as file:
        candidates_ = json.load(file)
    users = []
    if name:
        for candidate in candidates_:
            if name in candidate['name']:
                users.append(candidate['name'])
    return render_template('search_name.html', users=users, count=len(users))


@app.route('/skill/<skill>')
# Поиск по навыкам
def user_skills(skill):
    with open('candidates.json') as file:
        candidates_ = json.load(file)
    with open('settings.json') as file:
        # В зависимости от настройки limit выводим список людей с навыком Х
        settings = json.load(file)
    users = []
    count_skill = 0
    for candidate in candidates_:
        if skill in candidate['skills']:
            users.append(candidate['name'])
            count_skill += 1
            if settings['limit'] == count_skill:
                return render_template('search_name.html', users=users, count=len(users))
    return render_template('search_name.html', users=users, count=len(users))


app.run()
