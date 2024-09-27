from typing import List, Tuple, Any, Optional, Dict, Type
from sqlalchemy.exc import SQLAlchemyError
from app.models import db
from app.models.goods import ItemCategory
from sqlalchemy.orm import Session, aliased
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy import select, asc, desc



def handle_db_query_join(
    session: Session,
    primary_model: str,
    related_model: str, 
    primary_filters: Optional[Dict[str, Any]] = None,
    related_filters: Optional[Dict[str, Any]] = None,
    limit: Optional[int] = None,
    order_by: Optional[str] = None,
    descending: bool = False,
    many: bool = False
) -> Any:
    """Executes a database query with a join between the primary model and a related model.

    Args:
        session: SQLAlchemy session to use for the query.
        primary_model: The primary model to query.
        related_model: The related model to join with the primary model.
        primary_filters: Optional dictionary of filter options for the primary model.
        related_filters: Optional dictionary of filter options for the related model.
        limit: Optional limit on the number of results.
        order_by: Optional field name to order the results by.
        descending: Whether to order results in descending order.
        many: Whether to return many objects or just one.

    Returns:
        The result of the query. A single object or a list of objects.

    Raises:
        SQLAlchemyError: If the query execution fails.
    """
    related_alias = aliased(related_model)
    stmt = select(primary_model).join(related_alias)

    if primary_filters:
        for attribute, value in primary_filters.items():
            stmt = stmt.where(getattr(primary_model, attribute) == value)

    if related_filters:
        for attribute, value in related_filters.items():
            stmt = stmt.where(getattr(related_alias, attribute) == value)

    if order_by:
        order_column = getattr(primary_model, order_by)
        stmt = stmt.order_by(desc(order_column) if descending else asc(order_column))

    if limit:
        stmt = stmt.limit(limit)

    try:
        if many:
            return session.execute(stmt).scalars().all()
        else:
            return session.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError as error:
        session.rollback()
        raise


def handle_db_query(
    session: Session, 
    model: str, 
    filters: Optional[Dict[str, Any]] = None, 
    many: bool = False, 
    limit: Optional[int] = None, 
    order_by: Optional[str] = None, 
    descending: bool = False
) -> Any:
    """Executes a database query for the given model.

    Args:
        session: SQLAlchemy session to use for the query.
        model: The model to query.
        filters: Optional dictionary of filter options.
        many: Whether to return many objects or just one.
        limit: Optional limit on the number of results.
        order_by: Optional field name to order the results by.
        descending: Whether to order results in descending order.

    Returns:
        The result of the query. A single object or a list of objects.

    Raises:
        SQLAlchemyError: If the query execution fails.
    """
    stmt = select(model)

    if filters:
        for attribute, value in filters.items():
            stmt = stmt.where(getattr(model, attribute) == value)
    
    if order_by:
        order_column = getattr(model, order_by)
        stmt = stmt.order_by(desc(order_column) if descending else asc(order_column))
    
    if limit:
        stmt = stmt.limit(limit)

    try:
        if many:
            return session.execute(stmt).scalars().all()
        else:
            return session.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError as error:
        session.rollback()
        raise




def handle_db_commit(instance):
    try:
        db.session.add(instance)
        db.session.commit()
        return True
    except SQLAlchemyError as error:
        db.session.rollback()
        raise

def get_itemtype_choices() -> List[Tuple[str, str]]:
    """
    Returns a list of tuples containing the item type and its capitalized version.

    :return: List[Tuple[str, str]]
    """
    categories: List[ItemCategory] = ItemCategory.query.all()
    return [(category.comment, category.comment.capitalize()) for category in categories]
