from django.contrib.auth.models import User


def create_user(username, email, password):
    try:
        user = User.objects.get(username=username)
        print(f'{user.username} already exists')
        raise ValueError(f'{user.username} already exists')
    except User.DoesNotExist:
        pass
    user = User.objects.create_user(username, email, password)
    user.save()
    return user
