from datetime import datetime

import pytest
from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to
from checkers.http_checkers import check_status_code_http


def test_post_v1_account(account_helper, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password

    account_helper.register_user(login=login, email=email, password=password)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    assert_that(
        response, all_of(
            has_property('resource', has_property('login', starts_with('ya_kor'))),
            has_property('resource', has_property('registration', instance_of(datetime))),
            has_property(
                'resource', has_properties(
                    {
                        'rating': has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )


@pytest.mark.parametrize('login, email, password, expected_status_code, error_message, ', [
    ('y4564gh', 'y4564gh@12.ru', 'qwe', 400, 'Validation failed'),
    ('y43645tyh', '1114*33.ru', 'qwertty', 400, 'Validation failed'),
    ('y', '111@m.ru', 'qwertyuy', 400, 'Validation failed')],
                         ids=['short password', 'invalid email', 'invalid password'])
def test_post_v1_account_negative(account_helper, login, email, password, expected_status_code, error_message):
    login = login
    password = password
    email = email
    with check_status_code_http(expected_status_code, error_message):
        account_helper.register_user(login=login, password=password, email=email)
