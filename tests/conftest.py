from collections import namedtuple
from datetime import datetime
from random import randint
from pathlib import Path
from vyper import v

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

options = (
    'service.dm_api_account',
    'service.mailhog',
    'user.login',
    'user.password'
)


@pytest.fixture(scope='session', autouse=True)
def set_config(request):
    config = Path(__file__).joinpath('../../').joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f'{option}', request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    parser.addoption("--env", action='store', default='stg', help='run stg')

    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


@pytest.fixture
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get('service.mailhog'))
    mailhog_client = MailHogApi(configuration=mailhog_configuration)
    return mailhog_client


@pytest.fixture
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture
def account_helper(account_api, mailhog_api):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def auth_account_api(mailhog_api):
    dm_api_configuration = DmApiConfiguration(host=v.get('service.dm_api_account'), disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog_api)
    account_helper.auth_client(
            login=v.get('user.login'),
            password=v.get('user.password')
    )
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.now()
    data = now.strftime('%d_%m_%Y_%H_%M_%S')
    login = f'ya_kor_{data}'+str(randint(1, 10))
    password = v.get('user.password')
    email = f'{login}@gmail.ru'
    new_email = f'new_{login}_1@mail.com'
    new_password = 'fjghjkerth56573jkkj'

    User = namedtuple('User', ['login', 'password', 'email', 'new_email', 'new_password'])
    user = User(login, password, email, new_email, new_password)
    return user
