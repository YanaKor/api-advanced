# def test_delete_v1_account_login_all(account_helper, prepare_user):
#     login = prepare_user.login
#     password = prepare_user.password
#     email = prepare_user.email
#
#     account_helper.register_user(login=login, password=password, email=email)
#     account_helper.user_login(login=login, password=password)
#     account_helper.logout_user_from_all_device(login=login, password=password)
#
def test_delete_v1_account_login_all(auth_account_api):
    auth_account_api.logout_user_from_all_device()
