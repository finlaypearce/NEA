from flask import Blueprint, render_template, flash, redirect, url_for, request
from ..forms import EditProfileForm, TeacherCodeForm
from flask_login import current_user, login_required
from .login import requires_roles
from ..models import User, Practice
from NEA import db, app


profile = Blueprint('profile', __name__)


@profile.route('/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    practice = user.practice.order_by(Practice.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('profile.user', username=user.username, page=practice.next_num) \
        if practice.has_next else None
    prev_url = url_for('profile.user', username=user.username, page=practice.prev_num) \
        if practice.has_prev else None
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


@profile.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('student.student_dashboard'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('profile.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('profile.user', username=username))


@profile.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('student.student_dashboard'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('profile.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('profile.user', username=username))


@profile.route('/set_teacher_code', methods=['GET', 'POST'])
@login_required
@requires_roles(1)
def set_teacher_code():
    form = TeacherCodeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(teacher_code=form.teacher_code.data).first()
        username = user.username
        return redirect(url_for('profile.follow', username=username))
    return render_template('profile/set_teacher_code.html', title='Set Teacher Code', form=form)
