import unittest
from unittest.mock import patch
from app.utils.dboperation import handle_db_query


from sqlalchemy import select, asc, desc
from sqlalchemy.exc import SQLAlchemyError

class TestHandleDbQuery(unittest.TestCase):

    @patch('app.utils.dboperation.Session')
    def test_handle_db_query_many(self, mock_session):
        mock_session.return_value = mock_session()
        mock_session.return_value.execute.return_value = mock_session().scalars().all.return_value = [1, 2, 3]

        result = handle_db_query(mock_session.return_value, Base, many=True)

        mock_session.assert_called_once_with()
        mock_session.return_value.execute.assert_called_once_with(select(Base))
        self.assertEqual(result, [1, 2, 3])

    @patch('app.utils.dboperation.Session')
    def test_handle_db_query_single(self, mock_session):
        mock_session.return_value = mock_session()
        mock_session.return_value.execute.return_value = mock_session().scalar_one_or_none.return_value = 'result'

        result = handle_db_query(mock_session.return_value, Base, many=False)

        mock_session.assert_called_once_with()
        mock_session.return_value.execute.assert_called_once_with(select(Base))
        self.assertEqual(result, 'result')

    @patch('app.utils.dboperation.Session')
    def test_handle_db_query_with_filters(self, mock_session):
        mock_session.return_value = mock_session()
        mock_session.return_value.execute.return_value = mock_session().scalars().all.return_value = [1, 2, 3]
        filters = {'attribute': 'value'}

        result = handle_db_query(mock_session.return_value, Base, filters=filters)

        mock_session.assert_called_once_with()
        mock_session.return_value.execute.assert_called_once_with(select(Base).where(Base.attribute == 'value'))
        self.assertEqual(result, [1, 2, 3])

    @patch('app.utils.dboperation.Session')
    def test_handle_db_query_with_order_by(self, mock_session):
        mock_session.return_value = mock_session()
        mock_session.return_value.execute.return_value = mock_session().scalars().all.return_value = [1, 2, 3]
        order_by = 'attribute'
        descending = True

        result = handle_db_query(mock_session.return_value, Base, order_by=order_by, descending=descending)

        mock_session.assert_called_once_with()
        mock_session.return_value.execute.assert_called_once_with(select(Base).order_by(desc(Base.attribute)))
        self.assertEqual(result, [3, 2, 1])

    @patch('app.utils.dboperation.Session')
    def test_handle_db_query_with_limit(self, mock_session):
        mock_session.return_value = mock_session()
        mock_session.return_value.execute.return_value = mock_session().scalars().all.return_value = [1, 2, 3]
        limit = 2

        result = handle_db_query(mock_session.return_value, Base, limit=limit)

        mock_session.assert_called_once_with()
        mock_session.return_value.execute.assert_called_once_with(select(Base).limit(2))
        self.assertEqual(result, [1, 2])

    @patch('app.utils.dboperation.Session')
    def test_handle_db_query_with_exception(self, mock_session):
        mock_session.return_value = mock_session()
        mock_session.return_value.execute.side_effect = SQLAlchemyError()

        with self.assertRaises(SQLAlchemyError):
            handle_db_query(mock_session.return_value, Base)

        mock_session.assert_called_once_with()
        mock_session.return_value.execute.assert_called_once_with(select(Base))
        mock_session.return_value.rollback.assert_called_once()