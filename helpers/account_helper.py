import time
from json import loads
from retrying import retry

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


def retry_if_result_none(result):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(func):
    def wrapper(*args, **kwargs):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена номер {count}')
            token = func(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError('превышено количество попыток получения активационного токена')
            if token:
                return token
            time.sleep(3)
    return wrapper


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def auth_client(self, login: str, password: str):
        response = self.dm_account_api.login_api.post_v1_account_login(
            json_data={'login': login, 'password': password}
        )
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        reg_resp = self.dm_account_api.account_api.post_v1_account(json_data)
        assert reg_resp.status_code == 201, f'Пользователь не был создан {reg_resp.json()}'

        token = self.get_activation_token_by_login(login)
        assert token is not None, f'Токен для пользователя {login} не был получен'

        activate_resp = self.dm_account_api.account_api.put_v1_account_token(token)
        assert activate_resp.status_code == 200, f'Пользователь {login} не был активирован'
        return activate_resp

    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        login_resp = self.dm_account_api.login_api.post_v1_account_login(json_data)
        assert login_resp.status_code == 200, f'Пользователь {login} не смог авторизоваться'
        return login_resp

    def change_email(self, login: str, password: str, email: str):

        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data)
        assert response.status_code == 200, "email не был изменен"

        token = self.get_activation_token_by_login(login)
        assert token is not None, f"Токен для пользователя {login} не был получен"

    def user_login_403(self, login: str, password: str, remember_me: bool = True):

        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }

        login_resp = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        assert login_resp.status_code == 403, 'Пользователь смог авторизоваться'
        return login_resp

    def activation_user_after_change_email(self, email: str):

        token = self.get_new_activation_token_by_email(email)
        assert token is not None, f"Токен для пользователя {email} не получен"

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не активирован"

    def reset_user_password(self, login: str, email: str):
        json_data = {
            'login': login,
            'email': email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data)
        assert response.status_code == 200, 'Пароль не был сброшен'
        return response

    def get_token_after_reset_password(self, login: str):
        token = self.get_reset_token_by_login(login)
        assert token is not None, f"Токен для пользователя {login} не получен"
        return token

    def change_user_password(self, login: str, token: str, password: str, new_password: str):
        json_data = {
            "login": login,
            "token": token,
            "oldPassword": password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data)
        assert response.status_code == 200, 'Пароль не был изменен'
        return response

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_activation_token_by_login(self, login):
        token = None
        mail_resp = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in mail_resp.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token

    @retry(stop_max_attempt_number=5, retry_on_result=retry_if_result_none, wait_fixed=1000)
    def get_reset_token_by_login(self, login):
        token = None
        response = self.mailhog.mailhog_api.get_api_v2_messages()
        # pprint.pprint(response.json())
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = str(user_data.get('ConfirmationLinkUri')).split('/')[-1]
                break
        return token

    @retrier
    def get_new_activation_token_by_email(self, changed_email: str):
        token = None
        mail_resp = self.mailhog.mailhog_api.get_api_v2_messages()
        for item in mail_resp.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_email = item['Content']['Headers']['To'][0]
            if user_email == changed_email:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token
