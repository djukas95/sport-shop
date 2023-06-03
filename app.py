#Importovanje Flaska, MYSQL-a i heša--------------------
from flask import Flask, session, render_template, url_for, request, flash, redirect
from flask_mysqldb import MySQL
import yaml
from passlib.hash import sha256_crypt
#---------------------------------------

#Importovanje Bootstrap paketa
from flask_bootstrap import Bootstrap
#---------------------------------

#Importovanje WTF Formi--------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length
#-------------------------------------------

#Konfigurisanje Flaska i Bootstrapa
app = Flask(__name__)
app.config['SECRET_KEY'] = 'PythonZadatak'
bootstrap = Bootstrap(app)
#

#KONFIG MYSQLA (Potreban unos podataka Nemanjine baze)
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
mysql = MySQL(app)
#--------------------------


class RegisterForm(FlaskForm):
    FirstName = StringField('Unesite Vase ime', validators=[DataRequired()])
    LastName = StringField('Unesite Vase prezime', validators=[DataRequired()])
    email = StringField('Unesite Vasu email adresu', validators=[DataRequired()])
    username = StringField('Unesite željeno korisničko ime', validators=[DataRequired()])
    pswrd = PasswordField('Unesite željenu lozinku', validators=[DataRequired(), Length(min=8)])
    verifypswrd = PasswordField('Ponovo unesite lozinku', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Registracija', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Unesite korisničko ime', validators=[DataRequired()])
    pswrd = PasswordField('Unesite lozinku', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Log In', validators=[DataRequired()])

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        FirstName = request.form.get('FirstName')
        LastName = request.form.get('LastName')
        email = request.form.get('email')
        username = request.form.get('username')
        pswrd = sha256_crypt.hash(request.form.get('pswrd'))#Vrši se heširanje lozinke
        verify_pass = request.form.get('verifypswrd')
        #Provjerava da li u bazi podataka već postoji unesena email adresa
        if (cur.execute('SELECT * FROM users WHERE email = %s', [email])):
            flash('Email adresa vec postoji u bazi podataka, pokušajte da se prijavite', 'danger')
            return render_template('register.html', form=form)
        #Ako je ispravna sifra unesena oba puta komituje se u bazu
        if sha256_crypt.verify(verify_pass, pswrd) == True:
            cur.execute('INSERT INTO users(firstname, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)', [FirstName, LastName, username, email, pswrd])
            mysql.connection.commit()
            cur.close()
            return redirect('/login/')
        else:
            flash('Lozinke se ne podudaraju, pokušajte ponovo.', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


