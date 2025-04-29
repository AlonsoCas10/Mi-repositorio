from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'  # ¡Cambia esto en una aplicación real!

# Ejemplo de almacenamiento de usuarios (¡NO USAR EN PRODUCCIÓN!)
USUARIOS = {}

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recuérdame')
    submit = SubmitField('Iniciar sesión')

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired(), EqualTo('confirm', message='Las contraseñas deben coincidir')])
    confirm = PasswordField('Confirmar contraseña')
    submit = SubmitField('Registrarse')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in USUARIOS:
            error = 'El nombre de usuario ya está registrado'
            return render_template('register.html', form=form, error=error)
        else:
            USUARIOS[username] = password  # ¡PELIGRO: No seguro para producción!
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if username in USUARIOS and USUARIOS[username] == password:
            # ¡Autenticación exitosa! Aquí iría la lógica de Flask-Login
            return redirect(url_for('protegido'))
        else:
            error = 'Nombre de usuario o contraseña incorrectos'
            return render_template('login.html', form=form, error=error)
    return render_template('login.html', form=form)

@app.route('/protegido')
def protegido():
    return "<h1>¡Página protegida!</h1>"

@app.route('/')
def index():
    return render_template('index.html', titulo='Inicio')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
