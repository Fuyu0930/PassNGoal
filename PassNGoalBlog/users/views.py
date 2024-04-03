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


#Logout
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))
#account (update UserForm)