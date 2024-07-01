import allure


@allure.suite('Method validation tests PUT v1/account/password')
@allure.sub_suite('Positive tests')
class TestPutV1AccountPassword:
    @allure.title('Change user password')
    def test_put_v1_account_password(self, account_helper, prepare_user):
        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password
        new_password = prepare_user.new_password

        account_helper.register_user(login=login, password=password, email=email)
        account_helper.user_login(login=login, password=password)
        token = account_helper.reset_user_password(login=login, email=email)
        account_helper.change_user_password(login=login, token=token, password=password, new_password=new_password)
        account_helper.user_login(login=login, password=new_password)
