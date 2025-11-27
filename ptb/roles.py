TEST_ROLES = {
    000000000: "organizer",  # user_id: организатор
    000000000: "speaker",    # user_id: спикер
    # все остальные слушатели
    # 106118627 - мой id
}

def get_user_role(user_id):
    """
    Определяет роль пользователя по user_id
    Временная реализация - позже заменим на запрос к БД
    """
    return TEST_ROLES.get(user_id, "guest")