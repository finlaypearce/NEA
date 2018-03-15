from flask import Blueprint, render_template
from flask_login import login_required


student = Blueprint('student', __name__)


@student.route('/dashboard')
@login_required
def student_dashboard():
    practice = [
        {
            'author': {'username': 'John'},
            'body': '1 hour practice.'
        },
        {
            'author': {'username': 'Susan'},
            'body': '1.5 hours practice!'
        }
    ]
    return render_template('/student/s_dashboard.html', title='Student Dashboard', practice=practice)
