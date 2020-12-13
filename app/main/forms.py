from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField,ValidationError,PasswordField,ValidationError
from wtforms.validators import Required,Email,EqualTo
from ..models import User
from datetime import datetime

class BlogPost(FlaskForm):
    
    blog_title = StringField('Blog title',validators=[Required()])
    blog_author = StringField('Author:',validators=[Required()])
    blog_content = TextAreaField('Write your blog:')
    submit = SubmitField('Submit')
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Let people know more about you:',validators=[Required()])
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    text = TextAreaField('Leave a comment:',validators=[Required()])
    submit = SubmitField('Submit')