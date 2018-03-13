from flask import Blueprint, render_template, flash, redirect, url_for
from NEA.forms import LoginForm


login = Blueprint('login', __name__)


@login.route('/', methods=['GET', 'POST'])
def loginform():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember _me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('login.loginform'))  # temporary
    return render_template('/login/login.html', title='Log In', form=form)
