from pythontest import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    keywords = db.relationship('Keywords', backref='used_by', lazy=True, uselist=False)
    # uses = db.relationship('Keywords', secondary=user_keywords, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Keywords(db.Model):
    keyword_id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String)
    threshold = db.Column(db.Integer, default=3)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
