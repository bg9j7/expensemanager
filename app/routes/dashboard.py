from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.infodisplay import get_bank_transaction_history
from app.models import db
dashboard_bp = Blueprint('main', __name__)


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("content.html", user=current_user)

@dashboard_bp.route("/userinfo")
@login_required
def user_info_dashboard():
    history= get_bank_transaction_history(db, current_user.account_number)
    print(history)
    return render_template("content.html", user=current_user, history=history)

