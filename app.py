from flask import Flask, render_template, url_for

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
    #Dio za podesavanje slanja mejla na dugme
    return render_template('contact.html')
