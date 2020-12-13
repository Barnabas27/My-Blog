from flask import render_template,request,redirect,url_for,abort
from . import main
from ..models import Comment,User,Blog
from .forms import CommentForm,UpdateProfile,UpdateProfile,BlogPost
from flask_login import login_required, current_user
from .. import db,photos
from datetime import datetime

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    blogs = Blog.query.filter_by (user = user).all()
    
    if user is None:
        abort(404)
    return render_template('profile/profile.html',user = user, blogs=blogs)
    
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

@main.route('/user/<uname>/new_blog',methods = ['GET','POST']) 
@login_required
def new_blog():
    blog = BlogPost()
    if blog.validate_on_submit():
        # id
        title = blog.blog_title.data
        author = blog.blog_author.data
        content =blog.blog_content.data
        
        new_blog = Blog(blog_title=title,blog_author = author,blog_content = content)
        
        new_blog.save_blog()
        return redirect(url_for('/blogs'))
    title = 'New Blog'
    return render_template('new_blog.html',title = title, BlogPost = blog)
@main.route('/user/<uname>/blogs',methods = ['GET','POST'])
@login_required
def blogs():
    user = User.query.filter_by(username = uname).first()
    if request.method == 'POST':
        blog_title = request.form['title']
        blog_content = request.form['content']
        blog_author = request.form['author']
        new_blog = BlogPost(post_title=blog_title,content=blog_content, author = blog_author)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/blogs')
    else:
        all_posts = Blog.query.order_by(Blog.date_posted).all()
        return render_template('blogs.html',posts = all_posts,uname=user.username)
    
@main.route('/posts/delete/<int:id>') 
def delete(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)
    db.session.commit()
    return redirect('/blogs')
# chang the BlogPosts here to Blogs

@main.route('/posts/edit/<int:id>',methods = ['GET','POST'])
def edit(id):
    blog = Blog.query.get_or_404(id)
    if request.method == 'POST':
        blog.title = request.form['title']
        blog.author = request.form['author']
        blog.content = request.form['content']
        db.session.commit()
        return redirect('/blogs')
    else:
        return render_template('edit.html',post = post)
       
@main.route('/comment/<int:id>',methods= ['POST','GET'])

@login_required
def viewBlog(id):
    thisblog = Blog.getBlogId(id)
    comments = Comment.getComments(id)
    if request.args.get("like"):
        thisblog.likes = thisblog.likes + 1
        db.session.add(thisblog)
        db.session.commit()
        return redirect("/comment/{blog_id}".format(blog_id = id))
    elif request.args.get("dislike"):
        thisblog.dislikes = thisblog.dislikes + 1
        db.session.add(thisblog)
        db.session.commit()
        return redirect("/comment/{blog_id}".format(blog_id = id))
    commentForm = CommentForm()
    if commentForm.validate_on_submit():
        comment = commentForm.text.data
        newComment = Comment(comment = comment,user = current_user,blog_id = id)
        newComment.saveComment()
    return render_template('comment.html',commentForm = commentForm,comments = comments,blog = thisblog)