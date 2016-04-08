from flask.ext.wtf import Form
from wtforms import  StringField,PasswordField,SubmitField,SelectField,validators
from wtforms.validators import DataRequired, Email

class LoginForm(Form):
    email = StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),validators.Length(min=6, max=35)])
    submit = SubmitField('submit')

class SignUpForm(Form):
    firstname = StringField('firstname',validators=[DataRequired()])
    lastname = StringField('lastname',validators=[DataRequired()])
    gender = SelectField('gender',choices=[('M','Male'),('F','Female')])
    email =StringField('email',validators=[DataRequired(),Email()])
    password = PasswordField('password',validators=[DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('submit')
