from flask import Flask, render_template, url_for, redirect, flash
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

#To make secret key use secrets module
#import sectrets
#secrets.token_hex(16) (16 is the number of bytes)

app.config['SECRET_KEY'] = ''

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
        flash(f'Account created for{form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)





if __name__ == "__main__":
    app.run(debug=True)
