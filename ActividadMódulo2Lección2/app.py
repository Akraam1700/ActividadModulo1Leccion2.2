from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar una clave secreta para proteger las sesiones
app.config['SECRET_KEY'] = 'MiClaveSecreta123'  

# Formulario de registro
class RegistroForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        InputRequired(message="Este campo es obligatorio"), 
        Length(min=3, message="El nombre debe tener al menos 3 caracteres")
    ])
    correo = StringField('Correo', validators=[
        InputRequired(message="Este campo es obligatorio"), 
        Email(message="Por favor, ingresa un correo válido")
    ])
    contraseña = PasswordField('Contraseña', validators=[
        InputRequired(message="Este campo es obligatorio"), 
        Length(min=6, message="La contraseña debe tener al menos 6 caracteres")
    ])

# Ruta principal para mostrar el formulario
@app.route('/', methods=['GET', 'POST'])
def index():
    form = RegistroForm()
    if form.validate_on_submit():
        # Aquí procesas los datos del formulario, por ejemplo, guardándolos en una base de datos
        return redirect(url_for('success'))  # Redirige a una página de éxito
    return render_template('index.html', form=form)

# Ruta de éxito después del registro
@app.route('/success')
def success():
    return "Registro exitoso!"

if __name__ == '__main__':
    app.run(debug=True)
