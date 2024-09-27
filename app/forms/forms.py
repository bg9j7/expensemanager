
from typing import  Any, Optional
from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField, SelectField,DateField,FieldList,FormField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange
from app.models import db 
from app.models.user import User
from app.models.account import Account


class BaseForm(FlaskForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the form with placeholders for each field.

        This method is overridden from the parent class FlaskForm. It iterates
        over each field in the form and sets the 'placeholder' attribute of the
        field to the lowercase version of its label text. This is done to provide
        a default placeholder text for each field in the form.

        Args:
            *args: Positional arguments to pass to the parent class.
            **kwargs: Keyword arguments to pass to the parent class.

        Returns:
            None
        """
        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)

        # Iterate over each field in the form
        for field_name, field in self._fields.items():
            # If the field does not already have a render_kw attribute, create one
            if not field.render_kw:
                field.render_kw = {}

            # Set the 'placeholder' attribute of the field to the lowercase version
            # of its label text. This provides a default placeholder text for the field.
            field.render_kw['placeholder'] = f"{field.label.text.lower()}"



class LoginForm(BaseForm):
    username: StringField = StringField('Username', validators=[DataRequired()])
    password: PasswordField = PasswordField('Password', validators=[DataRequired()])
    remember_me: BooleanField = BooleanField('Remember Me')
    submit: SubmitField = SubmitField('Log In')

class RegistrationForm(BaseForm):
    username: StringField = StringField('Username', validators=[DataRequired()])
    email: StringField = StringField('Email', validators=[DataRequired(), Email()])
    password: PasswordField = PasswordField('Password', validators=[DataRequired()])
    password2: PasswordField = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit: SubmitField = SubmitField('Register')

    def validate_username(self, username: StringField) -> None:
        user: Optional[User] = db.session.execute(db.select(User).filter_by(username=username.data)).scalar_one_or_none()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email: StringField) -> None:
        user: Optional[User] = db.session.execute(db.select(User).filter_by(email=email.data)).scalar_one_or_none()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class RegisterBankForm(BaseForm):
    name: StringField = StringField('Name', validators=[DataRequired()])
    account: StringField = StringField('Account', validators=[DataRequired()])
    amount: FloatField = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit: SubmitField = SubmitField('Register')

    
    def validate_account(self, account: StringField) -> None:
        bank_account: Optional[Account] = db.session.execute(db.select(Account).filter_by(account_number=account.data)).scalar_one_or_none()
        if bank_account is not None:
            raise ValidationError('Account already exists.')

class DepositForm(BaseForm):
    amount: FloatField = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit: SubmitField = SubmitField('Deposit')

class RegisterItemForm(BaseForm):
    name: StringField = StringField('Name', validators=[DataRequired()])
    quantity: FloatField = FloatField('Quantity', validators=[DataRequired(), NumberRange(min=0.01)])
    price: FloatField = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    purchase_location: StringField = StringField('Purchase Location', validators=[DataRequired()])
    itemcategory: SelectField = SelectField('Item Category', choices=[])
    purchase_date: DateField = DateField('Purchase Date',default=date.today() ,validators=[DataRequired()])
    comment: StringField = StringField('Comment', validators=[DataRequired()])

class PurchaseForm(BaseForm):
    items:FieldList = FieldList(FormField(RegisterItemForm), min_entries=1)
    submit: SubmitField = SubmitField('Purchase')

    def __init__(self, num_items=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure the FieldList has exactly num_items entries
        while len(self.items) < num_items:
            self.items.append_entry()

class UpdateBankForm(BaseForm):
    action:SelectField = SelectField('Action', choices=[('deposit', 'Deposit'), ('withdraw', 'Withdraw')])
    name: StringField = StringField('Name', validators=[DataRequired()])
    account: StringField = StringField('Account', validators=[DataRequired()])
    amount: FloatField = FloatField('Amount', validators=[DataRequired(), NumberRange(min=0.01)])
    submit: SubmitField = SubmitField('Submit')
