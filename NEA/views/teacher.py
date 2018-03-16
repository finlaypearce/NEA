from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user
from .login import requires_roles
from ..forms import PracticeForm
from ..models import Practice
from NEA import db, app


teacher = Blueprint('teacher', __name__)


@teacher.route('/management')
@login_required
@requires_roles(2)
def student_management():
    students = current_user.followed_students().all()
    return render_template('teacher/management.html', title='Student Management', students=students)
