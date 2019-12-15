"""

These are the forms used on the site.
Each instance that requires input from the
user has a corresponding form.

"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from litlog.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed

# Form for register page
class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	first = StringField('First Name', validators=[DataRequired()])
	last = StringField('Last Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirmpassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	#Check if the username entered already exists
	def valid_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username already exists")

	#Check if the email entered already exists
	def valid_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email already exists")

# Form for login page
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Log in')

# Form to update user info
class UpdateProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	first = StringField('First Name', validators=[DataRequired()])
	last = StringField('Last Name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Change picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	#Check if the username entered already exists
	def valid_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("Username already exists")

	#Check if the email entered already exists
	def valid_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("Email already exists")

# Form for searching books
class SearchForm(FlaskForm):
	search = StringField('Book or Author', validators=[DataRequired()])
	submit = SubmitField('Search')

# Form for adding book reviews
class ReviewForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	author = StringField('Author', validators=[DataRequired()])
	rating = SelectField(u'Rating', choices=[(0, '---'), (1, '1-Hated it'), (2, '2-It was okay'), (3, '3-Liked it'), (4, '4-Really liked it'), (5, '5-LOVED IT')], coerce=int, validators = [DataRequired()])
	content = TextAreaField('Review', validators=[DataRequired()])
	submit = SubmitField('Add')