import allure
import pytest
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
from helpers.dm_db import DmDatabase


@allure.suite('Method validation tests POST v1/account')
class TestPostV1Account:
    @allure.sub_suite('Positive tests')
    @allure.title('Check registration new user')
    def test_post_v1_account(self, account_helper, prepare_user):
        db = DmDatabase('postgres', 'admin', '5.63.153.31', 'dm3.5')

        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_user(login=login, email=email, password=password)
        dataset = db.get_user_by_login(login=login)
        for row in dataset:
            assert row['Login'] == login, f'User {login} not registered'
            assert row['Activated'] is True, f'User {login} not activated'

        response = account_helper.user_login(login=login, password=password, validate_response=True)

        PostV1Account.check_response_values(response, name='ya_kor')
        db.delete_user_by_login(login=login)

    @allure.sub_suite('Negative tests')
    @allure.title('Register new user with invalid data')
    @pytest.mark.parametrize('login, email, password, expected_status_code, error_message, ', [
        ('y4564gh', 'y4564gh@12.ru', 'qwe', 400, 'Validation failed'),
        ('y43645tyh', '1114*33.ru', 'qwertty', 400, 'Validation failed'),
        ('y', '111@m.ru', 'qwertyuy', 400, 'Validation failed')],
                             ids=['short password', 'invalid email', 'invalid password'])
    def test_post_v1_account_negative(self, account_helper, login, email, password, expected_status_code,
                                      error_message):
        with check_status_code_http(expected_status_code, error_message):
            account_helper.register_user(login=login, password=password, email=email)

    @allure.sub_suite('Positive tests')
    @allure.title('Check activation already activated user')
    def test_post_v1_account_activate_already_active_user(self, account_helper, prepare_user):
        db = DmDatabase('postgres', 'admin', '5.63.153.31', 'dm3.5')

        login = prepare_user.login
        email = prepare_user.email
        password = prepare_user.password

        account_helper.register_user(login=login, email=email, password=password)
        for row in db.get_user_by_login(login=login):
            assert row['Activated'] is True, f'User {login} not activated'

        dataset = db.set_activation(login=login)
        # for row in dataset:

        db.delete_user_by_login(login=login)

