import allure

from dm_api_account.models.login_creds import LoginCredentials
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class LoginApi(RestClient):

    @allure.step('Authenticate via credentials')
    def post_v1_account_login(self, login_creds: LoginCredentials, validate_response=True):
        """
        Authenticate via credentials
        :param :
        :return:
        """
        response = self.post(
            path='/v1/account/login',
            json=login_creds.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step('Logout as current user')
    def delete_v1_account_login(self, **kwargs):
        """
        Logout as current user
        :param :
        :return:
        """
        logout_resp = self.delete(
            path='/v1/account/login',
            **kwargs
        )
        return logout_resp

    @allure.step('Logout from every device')
    def delete_v1_account_login_all(self, **kwargs):
        """
        Logout from every device
        :param:
        :return:
        """
        logout_resp = self.delete(
            path='/v1/account/login/all',
            **kwargs
        )
        return logout_resp
