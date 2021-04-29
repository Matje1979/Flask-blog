# <<<<<<< HEAD:flaskblog/routes.py
import os
from flask import render_template, url_for, redirect, flash, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
# =======
from flask import Flask, render_template, url_for, redirect, flash
from flaskblog.forms import (RegistrationForm, LoginForm, PostForm,
                             RequestResetForm, ResetPasswordForm
                             )
from flaskblog import app, bcrypt, db
from flask_login import login_user, current_user, logout_user, login_required
import secrets
from PIL import Image
from flask_mail import Message
from flaskblog import mail

##########Pagination##########
##Query example
"""
posts = Post.query.paginate() -> returns paginate object
Get total num of items in posts:
posts.total
Get current page:
posts.page
Set num of posts per page:
posts = Post.query.paginate(per_page=num)
Get posts from a particular page num
posts = Post.query.paginate(page=num)
"""
#In Django this is in separate file
#In Django render_template is just render. 
#url_for() is {% url 'route name' %}

@app.route('/') 
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int) #get page num from url. 1 is default, integers required.
    # posts = Post.query.all()
    #Order posts in descending order
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='about')

@app.route('/register', methods=['GET', 'POST'])
def register():
    #if a user is already logged in redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #Creating a hashed cerion of the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        #Put the record into the database
        db.session.add(user)
        db.session.commit()
        #In Django flash is messagess.success or messagess.error...
        flash(f'Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print ("user.password: ", user.password)
        print ("form.password.data: ", form.password.data)
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            #extract value of the next key if present in the url.
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))

        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        #     flash("You have been logged in!", "success")
        #     return render_template('login.html', title='Login', form=form)
        else:
            flash("Login unsuccesful. Please check your username and password", "danger")
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    #creating a random name for a image file to avoid potential name conflict with an existing file in database.
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename) #separating file name from its extension. To ignore file name just write underscore.
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #creating a path for saving the image.
    output_size = (125, 125)
    #resizing image
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            #updating user data
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit() #here we don't need to do something like db.session.add()
            #This is necessary because of the "Post Get redirect pattern"
            flash("Your account has been updated", "success")
            return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', 
        form=form, legend="New post")


#This is how to access a specific post
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title='Update_post', 
        form=form, legend="Update_post")

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

 
@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int) #get page num from url. 1 is default, integers required.
    user = User.query.filter_by(username=username).first_or_404()
    # posts = Post.query.all()
    #Order posts in descending order
    posts = Post.query.filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)

def send_reset_email(user):
    #accepts an argument concerning the expiry time 
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@demo.com',
                                            recipients=[user.email])
    #_external=True is here to get the absolute url instead of relative. Absolute url is needed because user needs to access the page from outside of the application.
    #If a message is too long, one can use a jinja2 template for a message here.
    msg.body = f'''To reset your password, visit the following link {url_for("reset_token", token=token, _external=True)} 
    If you did not make this request, ignore this email  and no changes will be made.
    '''
    mail.send(msg)

@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        #universal pattern: form.attribute.data
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #Creating a hashed cerion of the password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        #Put the record into the database
        user.password = hashed_password
        db.session.commit() 
        #In Django flash is messagess.success or messagess.error...
        flash(f'Your password has been updated! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
