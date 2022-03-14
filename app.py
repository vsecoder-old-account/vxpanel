from flask import Flask
from flask import render_template, flash
from flask import redirect, url_for
from flask import request, jsonify
from flask_login import LoginManager, login_required
from flask_login import login_user, current_user
from flask_login import logout_user, UserMixin
from api import *
import os, json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

login_manager = LoginManager(app)
login_manager.login_view = 'login_page'

class User(UserMixin):
    username = 'admin'
    password = 'admin'
    is_active = ''

@login_manager.user_loader
def load_user(username):
    if User.username == username:
        return User

@app.route("/login", methods=['GET', 'POST'])
def index():
	return render_template('login.html')

@app.route("/", methods=['GET', 'POST'])
def page():
    if current_user:
	    return render_template('index.html', data=stat())
    else:
        return render_template('login.html')

@app.route("/info", methods=['GET', 'POST'])
def info():
    if current_user:
	    return render_template('info.html', data=stat())
    else:
        return render_template('login.html')

@app.route("/logs", methods=['GET', 'POST'])
def logs():
    if current_user:
	    return render_template('logs.html', data=stat())
    else:
        return render_template('login.html')

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if current_user:
	    return render_template('settings.html', data=stat())
    else:
        return render_template('login.html')

@app.route("/ssh", methods=['GET', 'POST'])
def ssh():
    if current_user:
	    return render_template('ssh.html', data=stat())
    else:
        return render_template('login.html')

@app.route("/api", methods=['GET', 'POST'])
def api():
    return jsonify(stat())

@app.route("/test", methods=['GET', 'POST'])
def api2():
    return jsonify(test())

@app.route('/login', methods=['GET', 'POST'])
def login_page():
	login = request.form.get('username')
	password = request.form.get('password')

	if login and password:
		user = load_user(login)
		if user:
			login_user(user)

			return redirect('/page')
		else:
			flash('Не верны Логин/Пароль')
	else:
		pass
	return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('login_page'))

@app.errorhandler(404)
def not_found_error(error):
    return '404'

@app.errorhandler(500)
def server_error(error):
    return '500'

if __name__ == '__main__':
	port = int(os.environ.get("PORT", 8000))
	app.run(host='0.0.0.0', port=port)
