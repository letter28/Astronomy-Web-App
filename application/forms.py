from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from flask_wtf.csrf import CSRFProtect
from application import app
from application.db_models import User, Planet

csrf = CSRFProtect(app)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[
        DataRequired(message="Please input your email address."),
        Email()])
    password = PasswordField("Password", validators=[
        DataRequired(message="Please input your password."),
        Length(min=5, max=20)])
    remember_me = BooleanField(label="Remember me")
    submit = SubmitField(label="Login")


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Please enter your username.")])
    email = StringField("Email", validators=[
        DataRequired(message="Please enter your email address."),
        Email()])
    first_name = StringField("First name", validators=[DataRequired(message="Please enter your first name.")])
    last_name = StringField("Last name", validators=[DataRequired(message="Please enter your last name.")])
    password = PasswordField("Password", validators=[
        DataRequired(message="Please enter your password."),
        Length(min=5, max=20)])
    password_required = PasswordField("Confirm Password", validators=[
        DataRequired(message="Please confirm your password."),
        Length(min=5, max=20),
        EqualTo('password')])
    submit = SubmitField(label="Register")

    def validate_username(self, username):
        user = User.query.filter_by(user_name=username.data).first()
        if user is not None:
            raise ValidationError('That username is already in use. Please enter a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("That email is already registered. Please enter a different email address.")


class PlanetNewForm(FlaskForm):
    planet_name = StringField("Name of the planet", validators=[DataRequired()])
    home_star = StringField("Home star")
    distance = FloatField("Distance from home star")
    mass = FloatField("Mass", validators=[DataRequired()])
    diameter = FloatField("Diameter", validators=[DataRequired()])
    no_of_moons = IntegerField("Number of moons", validators=[DataRequired()])
    orbital_period = FloatField("Orbital period")
    submit = SubmitField(label="Add")

    def validate_planet_name(self, planet_name):
        planet = Planet.query.filter_by(planet_name=planet_name.data).first()
        if planet is not None:
            raise ValidationError('Planet by that name is already in the database. Please enter a different name.')
