# database:
#   dm3_5:
#     host: 5.63.153.31
#     port: 5432
#     database: dm3.5
#     user: postgres
#     password: admin

from helpers.dm_db import DmDatabase

import structlog

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          # sort_keys=True
                                          )
    ]
)


def test_db():
    db = DmDatabase('postgres', 'admin', '5.63.153.31', 'dm3.5')
    db.get_all_users()
