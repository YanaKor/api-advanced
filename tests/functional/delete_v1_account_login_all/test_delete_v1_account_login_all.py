import allure


@allure.suite('Method validation tests DELETE v1/account/login/all')
@allure.sub_suite('Positive test')
class TestPostV1AccountLoginAll:
    @allure.title('Logout from every device')
    def test_delete_v1_account_login_all(self, auth_account_api):
        auth_account_api.logout_user_from_all_device()
