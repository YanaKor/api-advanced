def test_get_v1_account(auth_account_api):
    auth_account_api.dm_account_api.account_api.get_v1_account()


def test_get_v1_account_nonauth(account_helper):
    account_helper.dm_account_api.account_api.get_v1_account()