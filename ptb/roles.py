from meetup_core.models.Models import User


def get_user_role(user_id: int) -> str:
    """
    Возвращает роль пользователя по ID
    """

    user = user = User.objects.filter(tg_id=user_id).first()

    if user:
        return user.user_role

    # Если нет юзера в бд -> создаем
    else:
        new_user = User(tg_id=user_id, user_role='guest')
        new_user.save()

    return 'guest'
