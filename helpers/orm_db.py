from sqlalchemy import select, delete
from helpers.orm_models import User

from orm.orm_client import OrmClient


class OrmDatabase:

    def __init__(self, user, password, host, database):
        self.db = OrmClient(user, password, host, database)

    def get_all_users(self):
        query = select([User])
        dataset = self.db.send_query(query)
        return dataset


    def get_user_by_login(self, login):
        query = select([User]).where(
            User.Login == login
        )
        dataset = self.db.send_query(query=query)
        return dataset

    def delete_user_by_login(self, login):
        query = delete(User).where(
            User.Login == login
        )
        dataset = self.db.send_bulk_query(query=query)
        return dataset