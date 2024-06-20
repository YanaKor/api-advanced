def test_put_v1_account_email(account_helper, prepare_user):

    login = prepare_user.login
    email = prepare_user.email
    password = prepare_user.password
    new_email = prepare_user.new_email

    account_helper.register_user(login=login, email=email, password=password)
    account_helper.user_login(login=login, password=password)
    account_helper.change_email(login=login, email=new_email, password=password)
    account_helper.user_login_403(login=login, password=password)
    account_helper.activation_user_after_change_email(email=new_email)
    account_helper.user_login(login=login, password=password)
