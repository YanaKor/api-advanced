from json import loads

from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi


class AccountHelper:
    def __init__(self, dm_account_api: DMApiAccount, mailhog: MailHogApi):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_user(self, login: str, password: str, email: str):
        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        reg_resp = self.dm_account_api.account_api.post_v1_account(json_data)
        assert reg_resp.status_code == 201, f'Пользователь не был создан {reg_resp.json()}'
        mail_resp = self.mailhog.mailhog_api.get_api_v2_messages()
        assert mail_resp.status_code == 200, f'Письма не получены {reg_resp.json()}'
        token = self.get_activation_token_by_login(login, mail_resp)
        assert token is not None, f'Токен для пользователя {login} не был получен'
        activate_resp = self.dm_account_api.account_api.put_v1_account_token(token)
        assert activate_resp.status_code == 200, f'Пользователь {login} не был активирован'
        return activate_resp

    def user_login(self, login: str, password: str, remember_me: bool = True):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': True,
        }

        login_resp = self.dm_account_api.login_api.post_v1_account_login(json_data)
        assert login_resp.status_code == 200, f'Пользователь {login} не смог авторизоваться'
        return login_resp

    @staticmethod
    def get_activation_token_by_login(login, response):
        token = None
        for item in response.json()['items']:
            user_data = loads(item['Content']['Body'])
            user_login = user_data['Login']
            if user_login == login:
                token = user_data['ConfirmationLinkUrl'].split('/')[-1]
        return token