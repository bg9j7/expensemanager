from typing import List,Any
from app.utils.dboperation import handle_db_query
from app.models.account import History

def get_bank_transaction_history(db: Any, account_number: str) -> List[History]:
    """
    Retrieves the transaction history for a bank account.

    Args:
        account_number: The account number of the bank account.
        user_id: The ID of the user.

    Returns:
        A list of History objects representing the transaction history.
    """
    filters = {'account_id': account_number}
    transaction_history = handle_db_query(
        db.session, History, filters=filters, many=True
    )
    return transaction_history
