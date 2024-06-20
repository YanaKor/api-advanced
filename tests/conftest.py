from collections import namedtuple
from datetime import datetime

import pytest
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

from helpers.account_helper import AccountHelper

import structlog


structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          # sort_keys=True
                                          )
    ]
)


@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def auth_account_api(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
            login='ya_kor_20_06_2024_18_23_54',
            password='5668hjghkjkn'
    )
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime('%d_%m_%Y_%H_%M_%S')
    login = f'ya_kor_{data}'
    password = '5668hjghkjkn'
    email = f'{login}@gmail.ru'
    new_email = f'new_{login}_1@mail.com'

    User = namedtuple('User', ['login', 'password', 'email', 'new_email'])
    user = User(login, password, email, new_email)
    return user
