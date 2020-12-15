from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from ..models import Comment,User,Blog,Subscriber
from .forms import CommentForm,UpdateProfile,UpdateProfile,BlogPost,SubscriberForm
from flask_login import login_required, current_user
from .. import db,photos
from datetime import datetime
from app.request import get_random_quotes
from wtforms import validators
from ..email import mail_message

@main.route('/')
def index():
    quotes = get_random_quotes()
    title = 'Home - Welcome To BeezBlog'
    return render_template('index.html',quotes = quotes,title = title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    
    
    if user is None:
        abort(404)
    return render_template('profile/profile.html',user = user)
    
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blogs/new_blog',methods = ['GET','POST']) 
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    blog_form = BlogPost()
    blog = Blog.query.order_by(Blog.date_posted.desc()).all()
    if blog_form.validate_on_submit():
        
        blog_title = blog_form.blog_title.data
        blog_author = blog_form.blog_author.data
        blog_content =blog_form.blog_content.data
        
        new_blog = Blog(title =blog_title ,author = blog_author,content = blog_content,user = current_user)
        
        db.session.add(new_blog)
        db.session.commit()
        
        for subscriber in subscribers:
            # mail_message('A new blog','email/new_blog',subscriber.email,new_blog=new_blog)
            return redirect(url_for('main.index'))
            flash = ('New Blog..Check it out')
    title = 'blogs'
    return render_template('new_blog.html',title = title, BlogPost = blog_form )

@main.route('/Update/<int:id>',methods = ['GET','POST'])
@login_required
def blogs():
    blogs = Blog.query.get_or_404(id)
    if blog.user != current_user:
        abort(404)
    form = BlogPost()
    if form.validate_on_submit():
        blogs.blog_title = form.blog_title.data
        blogs.blog_author = form.blog_author.data
        blogs.blog_content = form.blog_content.data
        db.session.commit()
        return redirect(url_for('main.blog'))
    elif request.method == 'GET':
        form.blog_title = form.blog_title
        form.blog_author = form.blog_author
        form.blog_content = form.blog_content
    return render_template('new_blog.html',form = form)
    
@main.route('/delete/<int:id>', methods=['GET','POST']) 
@login_required
def delete(id):
    blog = Blog.query.get_or_404(id)
    if blog.user != current_user:
        abort(404)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.blog'))
# chang the BlogPosts here to Blogs

@main.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def deleteComment(comment_id):
    comment =Comment.query.get_or_404(comment_id)
    if (comment.user.id) != current_user.id:
        abort(404)
    db.session.delete(comment)
    db.session.commit()
    flash('comment succesfully deleted')
    return redirect (url_for('main.blog'))

@main.route('/blogs/edit/<int:id>',methods = ['GET','POST'])
@login_required
def edit(id):
    blog = Blog.query.get_or_404(id)
    if request.method == 'POST':
        blog.title = request.form['title']
        blog.author = request.form['author']
        blog.content = request.form['content']
        db.session.commit()
        return redirect (url_for('main.blog'))
    else:
        return render_template('blogs.html',blog = blog)
    
@main.route('/blogs/allblogs',methods = ['GET','POST'])
@login_required
def blog():
    blog = Blog.query.all()
    print("Our results",blog)
    return render_template('blogs.html',blog=blog)
       
@main.route('/comment/<int:id>',methods= ['POST','GET'])

@login_required
def viewBlog(id):
    blog = Blog.query.get_or_404(id)
    comments = Comment.query.filter_by(blog_id = id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(blog_id = id).all()
        new_comment.save_comment()
     
    return render_template('comment.html',comment_form = comment_form,comments = comments,blog = blog)

@main.route('/subscribe',methods = ['GET','POST'])
def subscriber():
    quotes = get_random_quotes()
    subscriber_form = SubscriberForm()
    blog = Blog.query.order_by(Blog.date_posted.desc()).all()
    if subscriber_form.validate_on_submit():
        subscriber = Subscriber(email=subscriber_form.email.data,name = subscriber_form.name.data)
        
        db.session.add(subscriber)
        db.session.commit()
        
        mail_message('Welcome to BeezBlog','email/subscriber',subscriber.email,subscriber=subscriber)
        
        title = 'BeezBlog'
        return render_template('index.html',title=title, blog=blog,quotes = quotes)
    subscriber = Blog.query.all()
    blog = Blog.query.all()
    return render_template('subscribe.html',subscriber=subscriber,subscriber_form=subscriber_form,blog=blog)
    
    