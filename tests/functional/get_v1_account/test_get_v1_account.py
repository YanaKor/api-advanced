import allure
from datetime import datetime
from assertpy import assert_that, soft_assertions

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole
from checkers.get_v1_account import GetV1Account


@allure.suite('Method validation tests DELETE v1/account/login/all')
@allure.sub_suite('Positive test')
class TestGetV1Account:
    @allure.title('Get current user')
    def test_get_v1_account(self, auth_account_api):
        response = auth_account_api.dm_account_api.account_api.get_v1_account()
        GetV1Account.check_response_values(response, name='ya_kor')

    @allure.title('Get authorized user')
    def test_get_v1_account_auth(self, auth_account_api):
        response = auth_account_api.dm_account_api.account_api.get_v1_account()
        with soft_assertions():
            assert_that(response.resource.login).is_equal_to('ya_kor_20_06_2024_20_56_24')
            assert_that(response.resource.online).is_instance_of(datetime)
            assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)

    @allure.title('Get non-authorized user')
    def test_get_v1_account_nonauth(self, account_helper):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.dm_account_api.account_api.get_v1_account(validation_response=False)
