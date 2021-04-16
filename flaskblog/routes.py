<<<<<<< HEAD:flaskblog/routes.py
from flask import render_template, url_for, redirect, flash
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
=======
from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

#To make secret key use secrets module
#import sectrets
#secrets.token_hex(16) (16 is the number of bytes)

app.config['SECRET_KEY'] = ''
>>>>>>> d90f76ba8b1872f1a441a7e3f40a0e77bcaf00af:flaskblog.py

posts = [
{
    'author': 'Damir',
    'title': 'First post',
    'content': 'This is the first blog post',
    'date_posted': 'January 20, 2021'
},
{
    'author': 'Jane',
    'title': 'Second post',
    'content': 'This is the blog post',
    'date_posted': 'January 21, 2021'
    }
]


#In Django this is in separate file
#In Django render_template is just render. 
#url_for() is {% url 'route name' %}
@app.route('/') 
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='about')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        #In Django flash is messagess.success or messagess.error...
        flash(f'Account created for{form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash("You have been logged in!", "success")
            return render_template('login.html', title='Login', form=form)
        else:
            flash("Login unsuccesful. Please check your username and password", "danger")
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)