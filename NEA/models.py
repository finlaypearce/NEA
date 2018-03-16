from NEA import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from hashlib import md5


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    access = db.Column(db.Integer())
    about_me = db.Column(db.String(140))
    month_goal = db.Column(db.String(140))
    year_goal = db.Column(db.String(140))
    teacher_code = db.Column(db.Integer, unique=True)
    practice = db.relationship('Practice', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_entries(self):
        followed = Practice.query.join(
            followers, (followers.c.followed_id == Practice.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Practice.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Practice.timestamp.desc())

    def is_student(self):
        return self.access == 1

    def is_teacher(self):
        return self.access == 2

    def followed_students(self):
        students = User.query.join(followers, (followers.c.follower_id == User.id))\
            .filter(followers.c.followed_id == self.id)\
            .order_by(User.username.desc())
        return students

    def followed_s_entries(self):
        followed = Practice.query.join(
            followers, (followers.c.follower_id == Practice.user_id)).filter(
            followers.c.followed_id == self.id)
        return followed.order_by(Practice.timestamp.desc())


class Practice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    duration = db.Column(db.Integer)
    instrument = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Practice {}>'.format(self.body)
