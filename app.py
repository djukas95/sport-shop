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
        pswrd = request.form.get('pswrd')
        verify_pass = request.form.get('verifypswrd')
        #Provjerava da li se šifre podudaraju
        if pswrd==verify_pass:
            #Provjerava postoji li email u bazi podataka, ako nema komituje
            if (cur.execute('SELECT * FROM users WHERE email = %s', [email]) ==0):
                cur.execute('INSERT INTO users(firstname, lastname, username, email, password) VALUES (%s, %s, %s, %s, %s)', [FirstName, LastName, username, email, sha256_crypt.hash(pswrd)])
                mysql.connection.commit()
                cur.close()
                flash('Registration successful! Please login.', 'success')
                return redirect('/')
            else:
                flash('Email exists', 'danger')
                return render_template('register.html', form=form)
        else:
            flash('Password error', 'danger')
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)



@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if session.get('username') is None:
            cur = mysql.connection.cursor()
            username = request.form.get('username')
            pswrd = request.form.get('password')#Lenght is set to minimum 8 characters
            if (cur.execute('SELECT * FROM users WHERE username = %s', [username])) != 0:
                try:
                    cur.execute('SELECT password FROM users where username=%s', [username])
                    password = cur.fetchone()
                    if sha256_crypt.verify(pswrd , *password) == True:
                        session['login'] = True
                        session['username'] = request.form.get('username')
                        cur.execute('SELECT * FROM users WHERE username = %s', [username])
                        data = cur.fetchall()
                        session['FirstName'] = data[0]
                        session['LastName'] = data[1]
                        session['Username'] = data[2]
                        return redirect('/')
                    else:
                        flash('Password error', 'danger')
                        return render_template('login.html', form=form)
                except Exception as e:
                    flash(e)
                    return render_template('login.html', form=form)
            else:
                flash('Username not found.', 'danger')
                return render_template('login.html', form=form)
    return render_template('login.html', form=form)
            
        

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    if session['login'] == True:
        session.pop('Username', default=None)
        session.pop('FirstName', default=None)
        session.pop('LastName', default=None)
        session.pop('login',  default=False)
        #flash('Logged out!', 'success')
        return redirect('/')
    else:
        flash('No one is logged in', 'info')
        return render_template('index.html')