from flask import Blueprint, render_template, flash, redirect, url_for, session
from ..forms import LoginForm, StudentRegisForm, TeacherRegisForm
from flask_login import current_user, login_user, logout_user, login_required
from ..models import User
from NEA import db
from functools import wraps


login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def loginform():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login.loginform'))
        login_user(user, remember=form.remember_me.data)
        if user.access == 1 or user.access == 2:
            return redirect(url_for('student.student_dashboard'))
        # else (user.access == 3):
            # return redirect(url_for(admin page)
    return render_template('login/login.html', title='Log In', form=form)


@login.route('/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.loginform'))


@login.route('/studentregister', methods=['GET', 'POST'])
def studentregister():
    form = StudentRegisForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data, access=1)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered student!')
        return redirect(url_for('login.loginform'))
    return render_template('login/studentregister.html', title='Student Register', form=form)


@login.route('/teacherregister', methods=['GET', 'POST'])
def teacherregister():
    form = TeacherRegisForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data, access=2, teacher_code=form.teacher_code.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered teacher!')
        return redirect(url_for('login.loginform'))
    return render_template('login/teacherregister.html', title='Teacher Register', form=form)


def requires_roles(access):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user is None:
                flash('You must login before you access this page.')
                return redirect(url_for('login.loginform'))
            elif current_user.access != access:
                flash('You cannot access this page!')
                return redirect(url_for('student.student_dashboard'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
