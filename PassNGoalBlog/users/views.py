#users/views.py

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from PassNGoalBlog import db
from PassNGoalBlog.models import User, BlogPost
from PassNGoalBlog.users.forms import RegisterationForm, LoginForm, UpdateUserForm
from PassNGoalBlog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)
#register
@users.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegisterationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for the registeration')
        return redirect(url_for('users.login'))

    return render_template('register.html', form = form)

#Login
@users.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Every email should be unique. .first() could make sure the type is correct
        user = User.query.filter_by(email = form.email.data).first()

        # Assume the user enter the correct password
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Log in Success!')

            # Grab the information what user trying to access next
            next = request.args.get('next')

            if next == None or next[0] == '/':
                next = url_for('core.index')
            
            return redirect(next)
    
    return render_template('login.html', form = form)

#Logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))

#account (update UserForm)
@users.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        # If a user submit something in the picture file
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated!')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    user = User.query.filter_by(username=current_user.username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=1,per_page=3)

    profile_image = url_for('static', filename = 'profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image = profile_image, form = form, blog_posts = blog_posts)


#user's list of Blog posts
@users.route('/<username>')
def user_posts(username):
    # Get an integer value for the current page number from the query string
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page = 5)
    return render_template('user_blog_posts.html', blog_posts = blog_posts, user = user)
