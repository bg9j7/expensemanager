from typing import Optional, Union
from flask import Blueprint, render_template, request, redirect, url_for, flash,Response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db
from app.models.user import User
from app.forms.forms import LoginForm, RegistrationForm
from app.utils.dboperation import handle_db_commit, handle_db_query
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> Union[Response, str]:
    """
    Logs in a user.

    Returns:
        Union[Response, str]: If the user is already authenticated, redirect to the dashboard.
                               If the form is valid, redirect to the dashboard.
                               Otherwise, render the login template.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form: LoginForm = LoginForm()

    if form.validate_on_submit():
        filters = {'username': form.username.data}
        # Get the user from the database
        user = handle_db_query(db.session, User, filters)
       # user: Optional[User] = db.session.execute(db.select(User).filter_by(username=form.username.data)).scalar_one_or_none()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register() -> Union[Response, str]:
    """
    Registers a new user.

    Args:
        None

    Returns:
        Union[Response, str]: If the user is already authenticated, redirect to the dashboard.
                               If the form is valid, redirect to the login page.
                               Otherwise, render the registration template.
    """
    if current_user.is_authenticated:  # type: ignore
        return redirect(url_for('main.dashboard'))

    form: RegistrationForm = RegistrationForm()  # type: ignore

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        handle_db_commit(user)
        return redirect(url_for('auth.login'))

    return render_template('auth/registration.html', form=form)  # type: ignore

@auth_bp.route('/logout')
@login_required
def logout() -> Response:
    """
    Logs out the current user.

    Returns:
        Response: A redirect to the login page.
    """
    logout_user()
    return redirect(url_for('auth.login'))
