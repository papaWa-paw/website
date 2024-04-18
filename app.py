from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.recipes import Recipes
from forms.loginform import LoginForm
from data.users import User
from forms.resform import RecipesForm
from forms.user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/sign_in')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('sign_in.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('sign_in.html', title='Авторизация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/recipes_form',  methods=['GET', 'POST'])
@login_required
def recipes_form():
    form = RecipesForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = Recipes()
        news.title = form.title.data
        news.description = form.description.data
        news.ingredients = form.ingredients.data
        news.cooking = form.cooking.data
        news.type = form.type.data
        current_user.news.append(news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('recipes_form.html', title='Добавление новости', form=form)


@app.route('/recipes_form/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id):
    form = RecipesForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Recipes).filter(Recipes.id == id, Recipes.user == current_user).first()
        if news:
            form.title.data = news.title
            news.description = form.description.data
            news.ingredients = form.ingredients.data
            news.cooking = form.cooking.data
            news.type = form.type.data
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Recipes).filter(Recipes.id == id, Recipes.user == current_user).first()
        if news:
            news.title = form.title.data
            news.description = form.description.data
            news.ingredients = form.ingredients.data
            news.cooking = form.cooking.data
            news.type = form.type.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('recipes_form.html', title='Редактирование рецепта', form=form)


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(debug=True)
