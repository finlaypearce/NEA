from flask import Blueprint, render_template, flash, redirect, url_for
from NEA.forms import LoginForm
from flask_login import current_user, login_user, logout_user
from NEA.models import User


login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def loginform():

    #if current_user.is_authenticated:
        #return redirect(url_for('student.student_dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login.loginform'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('student.student_dashboard'))
    return render_template('/login/login.html', title='Log In', form=form)


@login.route('/')
def logout():
    logout_user()
    return redirect(url_for('login.loginform'))
