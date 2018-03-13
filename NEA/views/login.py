from flask import Blueprint, render_template
from NEA.forms import LoginForm


login = Blueprint('login', __name__)


@login.route('/')
def loginform():
    form = LoginForm()
    return render_template('/login/login.html', title='Sign In', form=form)
