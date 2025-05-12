from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed, Identity, AnonymousIdentity, identity_changed

app = Flask(__name__)
app.secret_key = 'clave_super_secreta'

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Configurar Flask-Principal
principals = Principal(app)

# Definir permisos por rol
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))

# Simulación de base de datos con hash y rol
usuarios = {
    'admin': {
        'password_hash': generate_password_hash('12345'),
        'rol': 'admin'
    },
    'editor': {
        'password_hash': generate_password_hash('editor123'),
        'rol': 'editor'
    },
    'johndoe': {
        'password_hash': generate_password_hash('secreto'),
        'rol': 'usuario'
    }
}

# Clase de usuario
class Usuario(UserMixin):
    def __init__(self, username):
        self.id = username

# Cargar usuario desde sesión
@login_manager.user_loader
def load_user(user_id):
    if user_id in usuarios:
        return Usuario(user_id)
    return None

# Identidad y permisos
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
        user_role = usuarios[current_user.id]['rol']
        identity.provides.add(RoleNeed(user_role))

# Ruta protegida: principal
@app.route('/')
@login_required
def home():
    return render_template('home.html', nombre=current_user.id)

# Ruta protegida solo para admin
@app.route('/admin')
@login_required
@admin_permission.require(http_exception=403)
def admin_area():
    return f"Hola {current_user.id}, bienvenido al panel de administrador."

# Ruta protegida solo para editor
@app.route('/editor')
@login_required
@editor_permission.require(http_exception=403)
def editor_area():
    return f"Hola {current_user.id}, bienvenido al panel de editores."

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in usuarios and check_password_hash(usuarios[username]['password_hash'], password):
            user = Usuario(username)
            login_user(user)
            identity_changed.send(app, identity=Identity(user.id))  # <- Importante para Flask-Principal
            return redirect(url_for('home'))

        return render_template("error.html", error_code=401, 
                               error_message="Invalid username or password."), 401

    return render_template('login.html')

# Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(app, identity=AnonymousIdentity())  # <- Limpiar identidad
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
