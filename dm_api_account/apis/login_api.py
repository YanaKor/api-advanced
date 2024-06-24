from restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(self, json_data):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        login_resp = self.post(
            path='/v1/account/login',
            json=json_data
        )
        return login_resp

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
