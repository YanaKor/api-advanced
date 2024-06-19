def attempt(n=5):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print('------------------')
            print(n)
            func(*args, **kwargs)
            print('------------------')
            return
        return wrapper
    return decorator


@attempt(n=6)
def my_print(name):
    print(f'Hello, {name}!')


my_print('you')
