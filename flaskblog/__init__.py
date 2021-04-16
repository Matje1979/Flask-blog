from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#To make secret key use secrets module
#import secrets
#secrets.token_hex(16) (16 is the number of bytes)

#To create a database, after creating models, go to python shell inside project dir and write 'from flaskblog import db'.
#Then write: db.create_all()
#Create a model instance: instance = Model(field1="value", field2="value"...)
#To commit it to the database do: db.session.add(instance) and then save it with db.session.commit()
#Query all instances of a model in SQLAlchemy: Model.query.all()
#Get first: Model.query.first() (in Django it is Model.objects.first())
#Filter results: Model.query.filter_by(username="Corey").all() (in Django: Model.objects.filter(username="Corey"))
#If we leave out .all() or .first() we will get only the query object.
#Get first from the filtered results: Model.query.filter_by(username='Corey').first()
#instance = Model.query.filter_by(username='Corey').first()  (in Django: Model.objects.filter(username="username").first())
#Get instance id: instance.id
#Get instance with specific id: Model.query.get(id) (in Django: Model.objects.get(id=id))
#to delete everything in the database: db.drop_all()
#To recreate the whole database structure: db.create_all (in Django: python manage.py makemigrations > python manage.py migrate)

app.config['SECRET_KEY'] = '6db1e708c19b8a49912519e306f5967c'
#Configuring database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #/// is the sign for a relative path to current directory in sqlite.
db = SQLAlchemy(app)