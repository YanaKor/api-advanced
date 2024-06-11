import requests


class AccountApi:

    def __init__(self, host, headers=None):
        self.host = host
        self.headers = headers

    def post_v1_account(self, json_data):
        """
        Register new user
        """
        reg_resp = requests.post(
            url=f'{self.host}/v1/account',
            json=json_data
        )
        return reg_resp

    def put_v1_account_token(self, token):
        """
        Activate registered user
        """
        headers = {
            'accept': 'text/plain',
        }
        activate_resp = requests.put(
            url=f'{self.host}/v1/account/{token}',
            headers=headers
        )
        return activate_resp
