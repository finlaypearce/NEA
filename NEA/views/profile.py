from flask import Blueprint, render_template, flash, redirect, url_for, request
from ..forms import EditProfileForm
from flask_login import current_user, login_required
from ..models import User
from NEA import db


profile = Blueprint('profile', __name__)


@profile.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    practice = [
        {'author': user, 'body': 'Test entry #1'},
        {'author': user, 'body': 'Test entry #2'}
    ]
    return render_template('profile/user.html', user=user, practice=practice)


@profile.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        current_user.month_goal = form.month_goal.data
        current_user.year_goal = form.year_goal.data

        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        form.month_goal.data = current_user.month_goal
        form.year_goal.data = current_user.year_goal
    return render_template('profile/edit_profile.html', title='Edit Profile', form=form)
