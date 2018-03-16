from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from .login import requires_roles
from ..forms import PracticeForm
from ..models import Practice, User, Level
from NEA import db, app, socketio
import math
import datetime
from flask_socketio import SocketIO, emit


student = Blueprint('student', __name__)


@student.route('/dashboard')
@login_required
def student_dashboard():
    page = request.args.get('page', 1, type=int)
    if current_user.access == 1:
        entries = current_user.followed_entries().paginate(
            page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('student.student_dashboard', page=entries.next_num) \
            if entries.has_next else None
        prev_url = url_for('student.student_dashboard', page=entries.prev_num) \
            if entries.has_prev else None
        practice = current_user.followed_entries().all()
        return render_template('student/s_dashboard.html', title='Student Dashboard',
                           practice=practice, entries=entries.items)

    elif current_user.access == 2:
        entries = current_user.followed_s_entries().paginate(
            page, app.config['POSTS_PER_PAGE'], False)
        next_url = url_for('student.student_dashboard', page=entries.next_num) \
            if entries.has_next else None
        prev_url = url_for('student.student_dashboard', page=entries.prev_num) \
            if entries.has_prev else None
        practice = current_user.followed_s_entries().all()
        return render_template('student/s_dashboard.html', title='Student Dashboard',
                           practice=practice, entries=entries.items)


@student.route('/record_practice', methods=['GET', 'POST'])
@login_required
@requires_roles(1)
def record_practice():
    form = PracticeForm()
    if form.validate_on_submit():
        time = form.hours.data*3600 + form.minutes.data*60
        entry = Practice(body=form.body.data, author=current_user, duration=time, instrument=form.instrument.data)

        s = current_user.get_streak()
        current_exp = current_user.get_exp()

        add_exp = math.floor((time*((s/100)+2)**((s/100)+1))/100)
        update_exp = current_exp + add_exp
        current_user.student_exp = update_exp

        latest_entry = Practice.query.filter_by(username=current_user.username)
        if datetime.datetime.now() - latest_entry.timestamp < 24:
            current_user.streak = current_user.streak + 1

        db.session.add(entry)
        db.session.commit()
        flash('Practice entry successfully made!')
        return redirect(url_for('student.student_dashboard'))
    return render_template('student/record_practice.html', title='Record Practice', form=form)


@student.route('/messages')
def messages():
    return render_template('student/messages.html')

@socketio.on('my event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']})

@socketio.on('my broadcast event', namespace='/test')
def test_message(message):
    emit('my response', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
