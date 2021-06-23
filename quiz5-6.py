from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PYTHON3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///anime.sqlite'
db = SQLAlchemy(app)

class studioghibli(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    producer = db.Column(db.String(30), nullable=False)
    release_date = db.Column(db.Float, nullable=False)
    running_time = db.Column(db.Float, nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('user'))

    return render_template('login.html')



@app.route('/user')
def user():
    subjects = ['My Neighbor Totoro', 'Spirited Away', 'Kiki’s Delivery Service', 'Castle in the Sky']
    return render_template('user.html',  subjects=subjects)


@app.route('/<name>/<age>')
def userage(name, age):
    return f'Hello {name}, your age is {age}'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'you are logged out'


@app.route('/anime', methods=['GET', 'POST'])
def anime():
    if request.method == 'POST':
        t = request.form['title']
        p = request.form['producer']
        re = request.form['release_date']
        ru = request.form['running_time']
        if t == '' or p == '' or re == '' or ru == '':
            flash('შეიყვანეთ ყველა ველი!', 'error')
        elif not re.isnumeric():
            flash('თარიღი და დრო უნდა იყოს რიცხვი!', 'error')
        elif not ru.isnumeric():
            flash('თარიღი და დრო უნდა იყოს რიცხვი!', 'error')
        else:
            a1 = studioghibli(title=t, producer=p, release_date=float(re), running_time=float(ru))
            db.session.add(a1)
            db.session.commit()
            flash('მონაცემები დამატებულია!', 'info')

    return render_template('anime.html')


if __name__ == "__main__":
    app.run(debug=True)