from flask import Flask, render_template, redirect, request, session, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from configparser import ConfigParser
from config import sqlalchemy_connection, secret_key
import logic

app = Flask(__name__)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('planets'))
    else:
        return render_template('index.html')


@app.route('/planets')
@app.route('/planets/')
@app.route('/planets/<page>')
@login_required
def planets(page=1):
    planets = logic.get_planets(page)
    if "results" in planets:
        return render_template('planets.html', planets=planets, name=current_user.username, user_id=current_user.id)
    else:
        abort(404)


@app.route('/statistics', methods=["POST"])
def statistics():
    return jsonify(logic.get_statistics())


@app.route('/vote', methods=["POST"])
def vote():
    data = request.form.to_dict()
    logic.add_vote(data)
    return 'vote added'


@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if 'remember' in request.form:
        remember = request.form["remember"]
    else:
        remember = False
    user = Users.query.filter_by(username=username).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('planets'))
    return render_template('index.html', login_error=True)


@app.route('/register', methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    password2 = request.form["password2"]

    if logic.username_valid(username) and logic.password_valid(password, password2) and logic.form_valid(username, password):
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        logic.add_user(username, hashed_password)
        return render_template('index.html', success=True)
    else:
        if not logic.password_valid(password, password2):
            registration_error = "Passwords are not the same"
        if not logic.username_valid(username):
            registration_error = "This username is already taken"
        if not logic.form_valid(username, password):
            registration_error = "Form validation error"

    return render_template('index.html', registration_error=registration_error)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html', logged_out=True)


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


if __name__ == "__main__":
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_connection()
    app.secret_key = secret_key()
    app.run(
        debug=True,
        port=5000
    )
