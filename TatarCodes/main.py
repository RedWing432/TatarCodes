from flask import Flask, render_template, redirect, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from forms.user import RegisterForm, LoginForm, TaskSendForm, InterprerForm
from data import db_session, users_api
from data.users import Users
from data.rating import Rating
from data.tasks import Task
from data.outputinput import Hp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def check(task_id, user_id):
    with open(f'static/tasks/{task_id}/user_solution_{user_id}.py', 'r') as f:
        lines = f.readlines()
        f.close()
    sess = db_session.create_session()
    inp = sess.query(Task).filter(Task.id == task_id).first().input_data

    newf = open(f'static/tasks/{task_id}/new_solution_{user_id}.py', 'w')
    data_to_write = "import sys\n" \
                    "stdout = sys.stdout\n" \
                    f"sys.stdin = {inp}\n" \
                    f"sys.stdout = open('user_output_{user_id}.txt', 'w')\n"
    newf.write(data_to_write)
    for line in lines:  # write old content after new
        newf.write(line)
    newf.close()


def translate(code_data):
    with open('data/translated.txt', encoding='utf-8') as file:
        data = [f.split() for f in file.read().split('\n')]
        d = {}
        for en, tat in data:
            d[tat] = en
        all_funcs = list(item[1] for item in data)

    s1 = 0
    s2 = 0
    slovo = ''
    res = ''
    for l in code_data:
        if l.isalpha():
            slovo += l

        else:
            if slovo and s1 == 0 and s2 == 0 and slovo in all_funcs:
                res += slovo.replace(slovo, d[slovo])
            else:
                res += slovo
            if l == '"':
                if s2:
                    s2 -= 1
                else:
                    s2 += 1
            elif l == "'":
                if s1:
                    s1 -= 1
                else:
                    s1 += 1
            res += l
            slovo = ''

    return (res)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(Users).get(user_id)


@app.route('/')
def index():
    return render_template('index.html', title='Tatar Codes')


@app.route('/dictionary')
def dictionary():
    with open('data/translated.txt', encoding='utf-8') as file:
        data = [words.split() for words in file.read().split('\n')]
    return render_template('dictionary.html', title='Сүзлек', data=data)


@app.route('/interpreter')
def interpreter():
    return render_template('inter.html', title='Интерпритатор')


@app.route('/interprete', methods=['POST'])
def interprete():
    code = request.form['code']
    code1 = translate(code)
    with Hp() as output:
        exec(code1)
    return render_template('inter.html', title='Интерпритатор', code=code, result='\n'.join(output))


@app.route('/task/<int:task_id>', methods=['POST', 'GET'])
def task(task_id):
    form = TaskSendForm()
    session = db_session.create_session()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_data = translate(form.code.data)
            with open(f'static/tasks/{task_id}/user_solution_{current_user.id}.py', 'w') as new_file:
                new_file.write(new_data)
            if check(task_id, current_user.id):
                solved = True
                msg = 'Шэп!'
            else:
                solved = False
                msg = 'Тагын бер тапкыр попробуй'
            return render_template('task.html')
        else:
            return redirect('/login')

    task = session.query(Task).filter(Task.id == task_id).first()
    return render_template('task.html', task=task, form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html',
                                   title="Регистрация",
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(Users).filter(Users.email == form.email.data).first():
            return render_template('register.html',
                                   title="Регистрация",
                                   form=form,
                                   message="Пользователь с такой почтой уже есть")

        user = Users(
            login=form.login.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')
    return render_template('register.html', form=form, title='Регистрация')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(Users).filter(Users.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html',
                               title='Авторизация',
                               form=form,
                               message='Неправильный логин или пароль')
    return render_template('login.html', form=form, title='Авторизация')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init('db/main.db')
    app.register_blueprint(users_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
