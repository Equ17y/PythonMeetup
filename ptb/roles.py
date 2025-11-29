from meetup_core.models import User


def get_user_role(user_id: int, username: str = None) -> str:
    """
    Возвращает роль пользователя по ID
    """

    user = User.objects.filter(tg_id=user_id).first()

    if user:
        if username and user.username != username:
            user.username = username
            user.save()
        return user.user_role

    # Если нет юзера в бд -> создаем
    else:
        new_user = User(tg_id=user_id, username=username, user_role='guest')
        new_user.save()

    return 'guest'
