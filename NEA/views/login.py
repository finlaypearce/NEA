from flask import Blueprint, render_template, flash, redirect, url_for
from NEA.forms import LoginForm, StudentRegisForm
from flask_login import current_user, login_user, logout_user, login_required
from NEA.models import User
from NEA import db


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
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.loginform'))


@login.route('/studentregister', methods=['GET', 'POST'])
def studentregister():
    form = StudentRegisForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Congratulations, you are now a registered student!')
        return redirect(url_for('login.loginform'))
    return render_template('/login/studentregister.html', title='Student Register', form=form)
