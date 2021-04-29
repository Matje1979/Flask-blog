#Since db is in the __init__.py file in the flaskblog package, we can import it from flaskblog, not from __main__
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flaskblog import db
from datetime import datetime
from flaskblog import db, login_manager, app
from flask_login import UserMixin

#The problem of circular import may arise.When we run python flaskblog.py in terminal. Terminal recognizes flaskblog as 'main'. So, when it reads the models.py 
# and encounters flaskblog it is something new, so it goes into flaskblog and reads it line by line, and when it comes to User, it says I don't know what this is.
#Because User is defined bellow the imports and so when the interpreter was in the models.py it did not get to that definition.
#If we change form flaskblog import db to from __main__ import db we get the error that db is not recognized.
#Check would happen if we move import of User and Post in flaskblog bellow db creation? Would that solve the problem? 
#What would happen if we were to run our app where flaskblog is not equal to __main__, say from python shell? What if we tried to import db from flaskblog?
#This is what would happen:
""">>> from flaskblog import db
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/damir/flask_blog/flaskblog.py", line 4, in <module>
    from models import User, Post
  File "/home/damir/flask_blog/models.py", line 1, in <module>
    from __main__ import db
ImportError: cannot import name 'db' from '__main__' (unknown location)"""

#In Django db.Model = models.Model and Column is Charfield?
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    #The following is not a column in the database, it is just an additional query running in the background - C.Shafer
    #In Django there is no such thing, I think.
    #backref allows us to access author from Post instance, although there is no such field in Post and only connection to user.id.
    posts = db.relationship('Post', cascade='all,delete', backref='author', lazy=True) #lazy=True just defines that SQLALchemy will load data as necessary in one go -C.Shafer
    
    #Method for creating secret key for password reset
    def get_reset_token(self, experies_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], experies_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    #Method for verifying the token
    #This is a static method because it does not refer anywhere to self. We need to tell python not to expect it.
    @staticmethod
    def verify_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
        
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

