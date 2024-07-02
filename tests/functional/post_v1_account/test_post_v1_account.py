import pytest
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_user(login=login, email=email, password=password)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    PostV1Account.check_response_values(response)


@pytest.mark.parametrize('login, email, password, expected_status_code, error_message, ', [
    ('y4564gh', 'y4564gh@12.ru', 'qwe', 400, 'Validation failed'),
    ('y43645tyh', '1114*33.ru', 'qwertty', 400, 'Validation failed'),
    ('y', '111@m.ru', 'qwertyuy', 400, 'Validation failed')],
                         ids=['short password', 'invalid email', 'invalid password'])
def test_post_v1_account_negative(account_helper, login, email, password, expected_status_code, error_message):
    with check_status_code_http(expected_status_code, error_message):
        account_helper.register_user(login=login, password=password, email=email)
