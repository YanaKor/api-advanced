from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(self, json_data):
        """
        Register new user
        :param json_data:
        :return:
        """
        reg_resp = self.post(
            path='/v1/account',
            json=json_data
        )
        return reg_resp

    def get_v1_account(self, **kwargs):
        """
        Get current user
        :return:
        """
        resp = self.get(
            path='/v1/account',
            **kwargs
        )
        return resp

    def put_v1_account_token(self, token):
        """
        Activate registered user
        param token:
        """
        headers = {
            'accept': 'text/plain',
        }
        activate_resp = self.put(
            path=f'/v1/account/{token}',
            headers=headers
        )
        return activate_resp

    def put_v1_account_email(self, json_data):
        """
        Change registered user email
        :param json_data:
        :return:
        """
        response = self.put(
            path='/v1/account/email',
            json=json_data
        )
        return response
