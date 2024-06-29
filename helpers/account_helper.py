import time
from json import loads
from retrying import retry

from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.login_creds import LoginCredentials
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
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
        response = self.user_login(login=login, password=password)
        token = {
            'x-dm-auth-token': response.headers['x-dm-auth-token']
        }
        self.dm_account_api.account_api.set_headers(token)
        self.dm_account_api.login_api.set_headers(token)

    def register_user(self, login: str, password: str, email: str):
        registration = Registration(
            login=login,
            password=password,
            email=email
        )

        reg_resp = self.dm_account_api.account_api.post_v1_account(registration=registration)
        assert reg_resp.status_code == 201, f'Пользователь не был создан {reg_resp.json()}'
        start_time = time.time()
        token = self.get_activation_token_by_login(login)
        end_time = time.time()
        assert end_time - start_time < 3, 'Время ожидания активации превышено'
        assert token is not None, f'Токен для пользователя {login} не был получен'

        activate_resp = self.dm_account_api.account_api.put_v1_account_token(token)
        return activate_resp

    def user_login(self, login: str, password: str, remember_me: bool = True, validate_response=False,
                   validate_headers=False):
        login_creds = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        login_resp = self.dm_account_api.login_api.post_v1_account_login(
            login_creds=login_creds, validate_response=validate_response)
        if validate_headers:
            assert login_resp.headers['x-dm-auth-token'], 'Токерн для пользователя не был получен'
            assert login_resp.status_code == 200, f'Пользователь {login} не смог авторизоваться'
        return login_resp

    def change_email(self, login: str, password: str, email: str):

        change_email = ChangeEmail(
            login=login,
            password=password,
            email=email
        )
        response = self.dm_account_api.account_api.put_v1_account_email(change_email=change_email)
        # assert response.status_code == 200, "email не был изменен"

        token = self.get_activation_token_by_login(login)
        assert token is not None, f"Токен для пользователя {login} не был получен"

        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        # assert response.status_code == 200, "Пользователь не активирован"
        return response

    def reset_user_password(self, login: str, email: str):
        reset_password = ResetPassword(
            login=login,
            email=email
        )
        response = self.dm_account_api.account_api.post_v1_account_password(reset_password=reset_password)
        assert response.status_code == 200, 'Пароль не был сброшен'

        token = self.get_reset_token_by_login(login)
        assert token is not None, f"Токен для пользователя {login} не получен"
        return token

    def change_user_password(self, login: str, token: str, password: str, new_password: str):
        change_password = ChangePassword(
            login=login,
            token=token,
            old_password=password,
            new_password=new_password
        )
        response = self.dm_account_api.account_api.put_v1_account_password(change_password=change_password)
        # assert response.status_code == 200, 'Пароль не был изменен'
        return response

    def logout_user(self, **kwargs):
        token = self.user_login(**kwargs)
        headers = {
            "x-dm-auth-token": token.headers["x-dm-auth-token"]
        }
        response = self.dm_account_api.login_api.delete_v1_account_login(headers=headers)
        assert response.status_code == 204, 'Пользователь не вышел из учетной записи'
        return response

    def logout_user_from_all_device(self, **kwargs):
        token = self.user_login(**kwargs)
        headers = {
            "x-dm-auth-token": token.headers["x-dm-auth-token"]
        }
        response = self.dm_account_api.login_api.delete_v1_account_login_all(headers=headers)
        assert response.status_code == 204, 'Пользователь не вышел из учетной записи на всех устройствах'
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
