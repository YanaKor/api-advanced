from datetime import datetime
from assertpy import assert_that, soft_assertions
# from hamcrest import assert_that, has_property, starts_with, all_of, instance_of, has_properties, equal_to

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import UserRole


#
# def test_get_v1_account(auth_account_api):
#     response = auth_account_api.dm_account_api.account_api.get_v1_account()
#     assert_that(
#         response, all_of(
#             has_property('resource', has_property('login', starts_with('ya_kor'))),
#             has_property('resource', has_property('online', instance_of(datetime))),
#             has_property(
#                 'resource', has_properties(
#                     {
#                         'rating': has_properties(
#                             {
#                                 "enabled": equal_to(True),
#                                 "quality": equal_to(0),
#                                 "quantity": equal_to(0)
#                             }
#                         )
#                     }
#                 )
#             )
#         )
#     )

def test_get_v1_account_auth(auth_account_api):
    response = auth_account_api.dm_account_api.account_api.get_v1_account()
    with soft_assertions():
        assert_that(response.resource.login).is_equal_to('ya_kor_20_06_2024_20_56_24')
        assert_that(response.resource.online).is_instance_of(datetime)
        assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)


def test_get_v1_account_nonauth(account_helper):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validation_response=False)
