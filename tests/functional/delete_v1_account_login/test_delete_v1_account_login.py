import allure


@allure.suite('Method validation tests DELETE v1/account/login')
@allure.sub_suite('Positive tests')
class TestDeleteV1AccountLogin:

    @allure.title('Logout as current user')
    def test_delete_v1_account_login(self, auth_account_api):
        auth_account_api.logout_user()
