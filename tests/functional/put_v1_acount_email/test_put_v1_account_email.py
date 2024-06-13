import pprint
from json import loads
from random import randint
from faker import Faker

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi

from tests.functional.post_v1_account.test_post_v1_account import get_activation_token_by_login


def test_put_v1_account_email():
    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    # регистрация пользователя
    fake = Faker()

    login = f'ya_kor_test{randint(5, 10000)}'
    email = f'{login}@mail.ru'
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    new_email = f'{login}_new@mail.ru'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    reg_resp = account_api.post_v1_account(json_data)
    print(reg_resp.status_code)
    print(reg_resp.text)
    assert reg_resp.status_code == 201, f'Пользователь не был создан {reg_resp.json()}'

    # получить письма из почтового ящика

    mail_resp = mailhog_api.get_api_v2_messages()
    print(mail_resp.status_code)
    print(mail_resp.text)
    assert mail_resp.status_code == 200, f'Письма не получены {mail_resp.json()}'

    # получить активационный токен
    token = get_activation_token_by_login(login, mail_resp)

    assert token is not None, f'Токен для пользователя {login} не был получен'

    # активация пользователя
    activate_resp = account_api.put_v1_account_token(token)
    print(activate_resp.status_code)
    print(activate_resp.text)
    assert activate_resp.status_code == 200, f'Пользователь {login} не был активирован'

    # авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    login_resp = login_api.post_v1_account_login(json_data)
    print(activate_resp.status_code)
    print(activate_resp.text)
    assert login_resp.status_code == 200, f'Пользователь {login} не смог авторизоваться'

    # изменение email
    json_data_new = {
        'login': login,
        'email': new_email,
        'password': password,
    }

    response = account_api.put_v1_account_email(json_data_new)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, 'email не был изменен'

    # авторизация по новому email
    login_resp = login_api.post_v1_account_login(json_data)
    print(login_resp.status_code)
    print(login_resp.text)
    assert login_resp.status_code == 403, f'Пользователь смог авторизоваться'

    # получение нового письма с измененным  email
    mail_resp = mailhog_api.get_api_v2_messages()
    pprint.pprint(mail_resp.status_code)
    # pprint.pprint(mail_resp.json())
    assert mail_resp.status_code == 200, f'Письма не получены {mail_resp.json()}'

    # получение нового токена
    new_token = get_new_activation_token_by_email(login, new_email, mail_resp)

    assert new_token is not None, f'Токен для пользователя {login} не был получен'

    # активация пользователя по новому токену
    activate_resp = account_api.put_v1_account_token(token)
    print(activate_resp.status_code)
    print(activate_resp.text)
    assert activate_resp.status_code == 200, f'Пользователь {login} не был активирован'

    # авторизация по новому email
    login_resp = login_api.post_v1_account_login(json_data)
    print(login_resp.status_code)
    print(login_resp.text)
    assert login_resp.status_code == 200, f'Пользователь не смог авторизоваться'

def get_new_activation_token_by_email(login, new_email, resp):
    token = None
    for item in resp.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        user_email = item['Content']['Headers']['To'][0]
        if user_login == login and user_email == new_email:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
