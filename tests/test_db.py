import structlog
from helpers.orm_db import OrmDatabase
from helpers.orm_models import User

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
    dataset = orm.get_user_by_login('yana_')
    row: User
    for row in dataset:
        print(row.Login)
        print(row.Name)
        print(row.Email)
        print(row.Activated)

    orm.db.close_connection()
