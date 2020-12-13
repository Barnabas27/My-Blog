from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    fullname = db.Column(db.String(255))
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    posts = db.relationship('Post',backref = 'user',lazy = 'dynamic')
    comment = db.relationship('Comment',backref = 'user',lazy = "dynamic")
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
        
    @password.setter
    def password(self,password):
        self.password_secure = generate_password_hash(password)
            
    def verify_password(self,password):
            return check_password_hash(self.password_secure,password)
        
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    def __repr__(self):
        return f'User {self.username}'
    
class Blog(db.Model):
    
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(100),nullable=False, default='unknown')
    date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    
    comments = db.relationship('Comment',backref = 'blog',lazy = 'dynamic')
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_blogs(cls,id):
        blog = Blog.query.filter_by(blog_id = id).all()
        return blog
    
class Quote:
    def __init__(self,quote):
        self.quote='http://quotes.stormconsultancy.co.uk/random.json'
        
        
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(500))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'))
    
    def saveComment(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def getComments(cls,blog):
        comments = Comment.query.filter_by(blog_id = blog).all()
        return comments
    
    
    