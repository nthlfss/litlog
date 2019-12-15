"""

This handles the database.
Here each table is set up to store
and maintain the data entered by users

"""

from litlog import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# This table has the login info for each user
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	first = db.Column(db.String(35), nullable=False)
	last = db.Column(db.String(35), nullable=False)
	email = db.Column(db.String(20), unique=True, nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.png')
	password = db.Column(db.String(20), nullable=False)
	reviews = db.relationship('Book', backref='writer', cascade="all,delete", lazy=True)

	def __repr__(self):
		return f"User('{self.username}', '{self.image_file}')"

# This table has the books reviewed by User
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Book('{self.title}', '{self.date_posted}')"