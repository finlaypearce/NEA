from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, NumberRange, InputRequired
from NEA.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class StudentRegisForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class TeacherRegisForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    instrument = SelectField('Instrument taught',
                             choices=[('piano', 'Piano'), ('guitar', 'Guitar'),
                                      ('violin', 'Violin'), ('drums', 'Drums')],
                             validators=[DataRequired()])
    teacher_code = IntegerField('Set teacher code', validators=[DataRequired()])
    submit = SubmitField('Register')


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    month_goal = TextAreaField("This month's goal", validators=[Length(min=0, max=140)])
    year_goal = TextAreaField("This year's goal", validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')


class PracticeForm(FlaskForm):
    body = TextAreaField('Description', validators=[Length(min=0, max=140)])
    timestamp = DateField('Date/time', validators=[DataRequired()], format='%d-%m-%Y')
    hours = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=24)])
    minutes = IntegerField(validators=[InputRequired(), NumberRange(min=0, max=60)])
    instrument = SelectField('Instrument practiced',
                             choices=[('piano', 'Piano'), ('guitar', 'Guitar'),
                                      ('violin', 'Violin'), ('drums', 'Drums')],
                             validators=[DataRequired()])
    submit = SubmitField('Submit')


class TeacherCodeForm(FlaskForm):
    teacher_code = IntegerField('Input teacher code', validators=[DataRequired()])
    submit = SubmitField('Submit')
