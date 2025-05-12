from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Base de datos simulada con hash de contraseña y rol
usuarios = {
    'admin': {
        'password_hash': generate_password_hash('12345'),
        'rol': 'admin'
    },
    'johndoe': {
        'password_hash': generate_password_hash('secreto'),
        'rol': 'usuario'
    }
}


class Usuario(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return Usuario(user_id)
    return None

@app.route('/')
@login_required
def home():
    return render_template('home.html', nombre=current_user.id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and check_password_hash(usuarios[username]['password_hash'], password):
            user = Usuario(username)
            login_user(user)
            return redirect(url_for('home'))
        
        return render_template("error.html", error_code=401, 
                               error_message="Invalid username or password."), 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
