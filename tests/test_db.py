import structlog
from helpers.orm_db import OrmDatabase

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          # sort_keys=True
                                          )
    ]
)

def test_orm():
    user = 'postgres'
    password = 'admin'
    host = '5.63.153.31'
    database = 'dm3.5'

    orm = OrmDatabase(user, password, host, database)
    # orm.get_all_users()
    orm.get_user_by_login('yana_')

    orm.db.close_connection()
