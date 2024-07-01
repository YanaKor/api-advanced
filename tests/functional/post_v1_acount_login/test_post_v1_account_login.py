import allure


@allure.suite('Method validation tests POST v1/account/login')
@allure.sub_suite('Positive tests')
class TestPostV1AccountLogin:
    @allure.title('Successful authorization of the registered user')
    def test_post_v1_account_login(self, account_helper, prepare_user):

        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_user(login=login, email=email, password=password)
        account_helper.user_login(login=login, password=password)
