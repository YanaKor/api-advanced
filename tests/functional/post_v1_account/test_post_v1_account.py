from datetime import datetime

from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to


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