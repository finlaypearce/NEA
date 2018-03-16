from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from ..forms import PracticeForm
from ..models import Practice
from NEA import db, app


student = Blueprint('student', __name__)


@student.route('/dashboard')
@login_required
def student_dashboard():
    page = request.args.get('page', 1, type=int)
    entries = current_user.followed_entries().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('student.student_dashboard', page=entries.next_num) \
        if entries.has_next else None
    prev_url = url_for('student.student_dashboard', page=entries.prev_num) \
        if entries.has_prev else None
    practice = current_user.followed_entries().all()
    return render_template('student/s_dashboard.html', title='Student Dashboard',
                           practice=practice, entries=entries.items)


@student.route('/record_practice', methods=['GET', 'POST'])
@login_required
def record_practice():
    form = PracticeForm()
    if form.validate_on_submit():
        time = form.hours.data*3600 + form.minutes.data*60
        entry = Practice(body=form.body.data, author=current_user, duration=time, instrument=form.instrument.data)
        db.session.add(entry)
        db.session.commit()
        flash('Practice entry successfully made!')
        return redirect(url_for('student.student_dashboard'))
    return render_template('student/record_practice.html', title='Record Practice', form=form)
