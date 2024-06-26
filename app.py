from flask import Flask, render_template, redirect, url_for, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.likes import Likes
from data.recipes import Recipes
from forms.loginform import LoginForm
from data.users import User
from forms.resform import RecipesForm
from forms.user import RegisterForm

UPLOAD_FOLDER = 'static/img/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    db_sess = db_session.create_session()
    recipe = db_sess.query(Recipes).all()
    return render_template('about.html', recipes=recipe)


@app.route('/my_recipes')
@login_required
def my_recipes():
    recipes = []
    db_sess = db_session.create_session()
    likes = db_sess.query(Recipes).filter(Recipes.user_id == current_user.id).all()
    for like in likes:
        recipes.append(like)
    return render_template("profile.html", recipes=recipes)


@app.route('/about/like/<int:id>', methods=['GET', 'POST'])
@login_required
def about_like(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Recipes).filter(Recipes.id == id).first()
    nolike = db_sess.query(Likes).filter(Likes.recipe_id == news.id, Likes.user_id == current_user.id).all()
    yelike = db_sess.query(Likes).filter(Likes.recipe_id == news.id, Likes.user_id == current_user.id).first()
    like = Likes(recipe_id=news.id, user_id=current_user.id)
    if news and not nolike:
        db_sess.add(like)
        db_sess.commit()
    else:
        db_sess.delete(db_sess.query(Likes).filter(Likes.id == yelike.id).first())
        db_sess.commit()
    return redirect('/about')


@app.route('/about/more/<int:id>')
def about_more(id):
    db_sess = db_session.create_session()
    recipe = db_sess.query(Recipes).filter(Recipes.id == id).first()
    author = db_sess.query(User).filter(User.id == recipe.user_id).first()
    return render_template('about_more.html', author=author, recipe=recipe)


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
        news.user_id = current_user.id
        db_sess.merge(current_user)
        db_sess.add(news)
        db_sess.commit()
        return redirect('/')
    return render_template('recipes_form.html', title='Добавление новости', form=form)


@app.route('/profile')
@login_required
def profile():
    recipes = []
    db_sess = db_session.create_session()
    likes = db_sess.query(Likes).filter(Likes.user_id == current_user.id).all()
    for like in likes:
        if db_sess.query(Recipes).filter(Recipes.id == like.recipe_id).first():
            recipes.append(db_sess.query(Recipes).filter(Recipes.id == like.recipe_id).first())
    return render_template("profile.html", recipes=recipes)


@app.route('/userava')
@login_required
def userava():
    img = None
    if not current_user.avatar:
        try:
            with app.open_resource(app.root_path + url_for('static', filename='img/default.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            print("Не найден аватар по умолчанию: " + str(e))
    else:
        img = current_user.avatar
    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


if __name__ == '__main__':
    db_session.global_init("db/blogs.db")
    app.run(debug=True)
