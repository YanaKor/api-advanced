import pprint
from json import loads
from random import randint
from faker import Faker
import structlog
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

from helpers.account_helper import AccountHelper

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          # sort_keys=True
                                          )
    ]
)


def test_put_v1_account_email():

    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051',  disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    fake = Faker()

    login = f'ya_kor_test{randint(5, 10000)}'
    email = f'{login}@mail.ru'
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    new_email = f'{login}_new@mail.ru'

    account_helper.register_user(login=login, email=email, password=password)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login, email=new_email, password=password)
    account_helper.user_login_403(login=login, password=password)
    account_helper.activation_user_after_change_email(email=new_email)
    account_helper.user_login(login=login, password=password)
