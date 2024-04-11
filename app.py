from flask import Flask, render_template, request
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        pass
    else:
        return render_template('registration.html')


@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')


@app.route('/recipes_form')
def recipes_form():
    return render_template('recipes_form.html')


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(debug=True)
