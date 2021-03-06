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
    blogs = db.relationship('Blog',backref = 'user',lazy = 'dynamic')
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
    def load_user(users_id):
        return User.query.get(int(users_id))
        
    
    
    def __repr__(self):
        return f'User {self.username}'
    
class Blog(db.Model):
    
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(100),nullable=False, default='unknown')
    date_posted = db.Column(db.DateTime,nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id',ondelete = 'CASCADE'),nullable = False)
    comments = db.relationship('Comment',backref = 'blog',lazy = 'dynamic')
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
        
    def deleteBlog(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_blogs(cls,id):
        blogs = Blog.query.filter_by(id = id).all()
        return blogs
   
    
    def __repr__(self):
        return f'Blogs {self.title}'
 
        
class Comment(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id',ondelete = 'CASCADE'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id',ondelete = 'CASCADE'))
    posted = db.Column(db.DateTime, default = datetime.utcnow)
    
    def saveComment(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def getComments(cls,blog_id):
        comments = Comment.query.filter_by(blog_id = blog_id).all()
        return comments
    
    def deleteComment(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User {self.comment}'
    
class Subscriber(UserMixin, db.Model):
   __tablename__="subscribers"

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(255))
   email = db.Column(db.String(255),unique = True,index = True)


   def save_subscriber(self):
       db.session.add(self)
       db.session.commit()

   @classmethod
   def get_subscribers(cls,id):
       return Subscriber.query.all()


   def __repr__(self):
       return f'User {self.email}'
    