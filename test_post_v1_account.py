import pprint

import requests
from json import loads


def test_post_v1_account():
    # регистрация пользователя
    login = 'ya_kor_test2'
    email = f'{login}@mail.ru'
    password = '32545gtth'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    reg_resp = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)
    assert reg_resp.status_code == 201, f'Пользователь не был создан {reg_resp.json()}'

    # получить письма из почтового ящика

    params = {
        'limit': '50',
    }

    mail_resp = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)

    assert mail_resp.status_code == 200, f'Письма не получены {reg_resp.json()}'

    # получить активационный токен
    token = None
    for item in mail_resp.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]

    assert token is not None, f'Токен для пользователя {login} не был получен'

    # активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    activate_resp = requests.put(f'http://5.63.153.31:5051/v1/account/{token}', headers=headers)
    assert activate_resp.status_code == 200, f'Пользователь {login} не был активирован'

    # авторизация
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    login_resp = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    assert login_resp.status_code == 200, f'Пользователь {login} не смог авторизоваться'
