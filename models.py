import yaml, os.path
from .app import db
from flask_login import UserMixin


import yaml, os.path
Books = yaml.safe_load(
    open(
    os.path.join(
        os.path.dirname(__file__),
        "data.yml"
        )
    )
)
 
class Author (db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.String(100))

    def __repr__ (self ):
        return "Autheur (%d) %s" % (self.id , self.name)
    

class Book(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    price = db.Column(db.Float)
    url  = db.Column(db.String(500))
    image = db.Column(db.String(200))
    title = db.Column(db.String(100))
    author_od = db.Column(db.Integer, db.ForeignKey("author.id"))
    author = db.relationship("Author", backref=db.backref("books", lazy="dynamic"))

    def __repr__(self):
        return "Livre (%d) %s" % (self.id, self.title)
    
class Genre(db.Model):
    id_genre = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(500))
    
    def __repr__(self):
        return "Genre (%d) %s" % (self.id_genre, self.description)

def get_sample():
    return Book.query.limit(25).all()

def get_author(id):
    return Author.query.get_or_404(id)

def get_genre(id_genre):
    return Genre.query.get_or_404(id_genre)


class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))
    def get_id(self):
        return self.username

from .app import login_manager
@login_manager.user_loader
def load_user(username):
    return User.query.get(username)