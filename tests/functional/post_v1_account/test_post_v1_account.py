from json import loads
from random import randint

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi
import structlog
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4,
                                          ensure_ascii=True,
                                          # sort_keys=True
                                          )
    ]
)


def test_post_v1_account():
    # регистрация пользователя
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051',  disable_log=False)
    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api = MailhogApi(configuration=mailhog_configuration)

    login = f'ya_kor_test{randint(5, 10000)}'
    email = f'{login}@mail.ru'
    password = '5668hjghkjkn'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    reg_resp = account_api.post_v1_account(json_data)
    assert reg_resp.status_code == 201, f'Пользователь не был создан {reg_resp.json()}'

    # получить письма из почтового ящика

    mail_resp = mailhog_api.get_api_v2_messages()

    assert mail_resp.status_code == 200, f'Письма не получены {reg_resp.json()}'

    # получить активационный токен
    token = get_activation_token_by_login(login, mail_resp)

    assert token is not None, f'Токен для пользователя {login} не был получен'

    # активация пользователя
    activate_resp = account_api.put_v1_account_token(token)
    assert activate_resp.status_code == 200, f'Пользователь {login} не был активирован'

    # авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    login_resp = login_api.post_v1_account_login(json_data)
    assert login_resp.status_code == 200, f'Пользователь {login} не смог авторизоваться'


def get_activation_token_by_login(login, response):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
