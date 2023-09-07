from flask import Flask, render_template, url_for, request, session, flash

#BOOTSTRAP i APP FLASK
from flask_bootstrap import Bootstrap
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'Ratkos00!!'
#-------------------------------

@app.route('/about/', methods= ['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/contact/', methods= ['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if session.get('username') != True:
            flash('No user detected, please consider registering', 'info')
        else:
            return render_template('contact.html')
    return render_template('contact.html')
