from datetime import date
from flask import Blueprint, render_template, redirect, url_for, flash
from app.forms.forms import RegisterBankForm, RegisterItemForm, PurchaseForm, UpdateBankForm
from app.models.account import Account
from app.models.goods import Purchase, Items
from app.models import db
from flask_login import login_required, current_user
from app.utils.dboperation import handle_db_commit,handle_db_query,get_itemtype_choices
registration_bp= Blueprint('registrations', __name__)


@registration_bp.route('/addbank', methods=['GET', 'POST'])
@login_required
def addbank():
    form = RegisterBankForm()
    if form.validate_on_submit():  # check if form is valid
        account = Account(name=form.name.data, balance=form.amount.data,account_number=form.account.data,
                          user_id=current_user.id)
        handle_db_commit(account)
        return redirect(url_for('main.dashboard'))

    return render_template('/registrations/addbank.html', form=form)
@registration_bp.route('/additem', methods=['GET', 'POST'])
@login_required
def additem() -> "flask.Response":
    """
    Adds a new item purchase to the database.

    Returns:
        flask.Response: The rendered template for adding items.
    """
    form: "PurchaseForm" = PurchaseForm()
    form.items[0].itemcategory.choices = get_itemtype_choices()  # type: ignore

    if form.validate_on_submit():
        purchase: "Purchase" = Purchase(user_id=current_user.id)
        handle_db_commit(purchase)
        for item in form.items:
            name: str = item.data['name']
            quantity: float = item.data['quantity']
            price: float = item.data['price']
            purchase_location: str = item.data['purchase_location']
            itemcategory: int = item.data['itemcategory']
            purchase_date: date = item.data['purchase_date']
            comment: str = item.data['comment']

            item: "Items" = Items(
                purchase_id=purchase.id,
                name=name,
                quantity=quantity,
                price=price,
                purchase_location=purchase_location,
                purchase_date=purchase_date,
                comment=comment,
                item_category_id=itemcategory
            )
            handle_db_commit(item)

    return render_template('/registrations/additems.html', form=form)

@registration_bp.route('/updatebank', methods=['GET', 'POST'])
@login_required
def update_bank():
    form = UpdateBankForm()
    if form.validate_on_submit():
        account_number = form.account.data
        action = form.action.data
        amount = form.amount.data
        account = handle_db_query(db.session, Account,filters={'account_number': account_number}, many=False)
        if action == 'deposit':
            print(action)
            account.add(amount)
            handle_db_commit(account)
        elif action == 'withdraw':
            account.deduct_balance(amount)
            handle_db_commit(account)
        return redirect(url_for('main.dashboard'))

    return render_template('/registrations/updatebank.html', form=form)


@registration_bp.route('/managebankaccount', methods=['GET', 'POST'])
@login_required
def managebankaccount():
    banks = handle_db_query(db.session, Account, filters={'user_id': current_user.id}, many=True)
    return render_template('/registrations/manageaccount.html', banks=banks)