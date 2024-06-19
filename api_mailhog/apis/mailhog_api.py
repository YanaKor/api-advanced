from restclient.client import RestClient


class MailhogApi(RestClient):

    def get_api_v2_messages(self, limit=50):
        """
        Get users emails
        :param limit:
        :return:
        """
        params = {
            'limit': limit,
        }
        mail_resp = self.get(
            path='/api/v2/messages',
            params=params,
            verify=False
        )
        return mail_resp
