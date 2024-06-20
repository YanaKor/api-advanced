def test_put_v1_account_password(account_helper, prepare_user):
    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_password = prepare_user.new_password

    account_helper.register_user(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.reset_user_password(login=login, email=email)

    account_helper.auth_client(login=login, password=password)
    token = account_helper.get_token_after_reset_password(login=login)
    account_helper.change_user_password(login=login, token=token, password=password, new_password=new_password)
    account_helper.user_login(login=login, password=new_password)
