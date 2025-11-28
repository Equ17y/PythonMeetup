from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

# Часовой пояс Москвы
MOSCOW_TZ = ZoneInfo("Europe/Moscow")

# Хранилище завершённых докладов:
_FINISHED_SESSIONS: set[tuple[int, int]] = set()


def now_moscow() -> datetime:
    """Возвращает текущее московское время."""
    return datetime.now(MOSCOW_TZ)


def is_active_now(event_date, start_time) -> bool:
    """
    Проверяет, наступило ли время начала (по Москве).
    Для доклада мы НЕ ограничиваемся временем конца — доклад
    может идти дольше расписания.
    """
    start_dt = datetime.combine(event_date, start_time, tzinfo=MOSCOW_TZ)
    current = now_moscow()
    return current >= start_dt


def mark_session_finished(event_id: int, session_index: int) -> None:
    """
    Помечает доклад как завершённый спикером.
    Вызывается из обработчика кнопки «Завершить свое выступление».
    """
    _FINISHED_SESSIONS.add((event_id, session_index))


def is_session_finished(event_id: int, session_index: int) -> bool:
    """Проверяет, помечен ли доклад как завершённый спикером."""
    return (event_id, session_index) in _FINISHED_SESSIONS


# Можно использовать при перезапуске/тестах
def reset_finished_sessions() -> None:
    """Сбрасывает информацию о завершённых докладах."""
    _FINISHED_SESSIONS.clear()


def get_today_events():
    """
    Возвращает список сегодняшних мероприятий с полем is_active,
    которое определяется по программе докладов.
    """
    today = now_moscow().date()

    events = [
        {
            "id": 1,
            "name": "Тема мероприятия #1",
            "event_date": today,
            "started_at": time(10, 0),
            "ended_at": time(13, 0),
        },
        {
            "id": 2,
            "name": "Тема мероприятия #2",
            "event_date": today,
            "started_at": time(13, 0),
            "ended_at": time(16, 0),
        },
        {
            "id": 3,
            "name": "Тема мероприятия #3",
            "event_date": today,
            "started_at": time(16, 0),
            "ended_at": time(19, 0),
        },
    ]

    # Определяем активность мероприятия по активному докладу
    for event in events:
        program = get_event_program(event["id"])
        event["is_active"] = any(s.get("is_active") for s in program)

    return events


def _get_program_template():
    """
    Базовые данные программы мероприятия (без статусов).
    В реальном приложении это будет из БД.
    """
    return {
        1: [
            {
                "started_at": time(10, 0),
                "ended_at": time(11, 0),
                "topic": "Тема доклада #1",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
            {
                "started_at": time(11, 0),
                "ended_at": time(12, 0),
                "topic": "Тема доклада #2",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
            {
                "started_at": time(12, 0),
                "ended_at": time(13, 0),
                "topic": "Тема доклада #3",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
        ],
        2: [
            {
                "started_at": time(13, 0),
                "ended_at": time(14, 0),
                "topic": "Тема доклада #1",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
            {
                "started_at": time(14, 0),
                "ended_at": time(15, 0),
                "topic": "Тема доклада #2",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
            {
                "started_at": time(15, 0),
                "ended_at": time(16, 0),
                "topic": "Тема доклада #3",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
        ],
        3: [
            {
                "started_at": time(16, 0),
                "ended_at": time(17, 0),
                "topic": "Тема доклада #1",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
            {
                "started_at": time(17, 0),
                "ended_at": time(18, 0),
                "topic": "Тема доклада #2",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
            {
                "started_at": time(18, 0),
                "ended_at": time(19, 0),
                "topic": "Тема доклада #3",
                "speaker": "Иван Петров",
                "speaker_username": "@Nyuta12",
            },
        ],
    }


def get_event_program(event_id):
    """
    Возвращает программу мероприятия с двумя статусами:
    - is_finished: завершён ли доклад спикером
    - is_active: доклад, который «идёт сейчас»
      (учитывается московское время и завершённость предыдущего доклада)
    """
    now_dt = datetime.now(MOSCOW_TZ)
    today = now_dt.date()
    
    today = now_moscow().date()
    base_programs = _get_program_template()

    # Копируем, чтобы не портить шаблон
    raw_program = base_programs.get(event_id, [])
    program = [dict(item) for item in raw_program]

    # Сначала проставим is_finished
    for idx, item in enumerate(program):
        # Пометка завершён ли вручную
        finished_manually = is_session_finished(event_id, idx)

        # Автоматическое завершение через 30 минут после окончания
        event_end_dt = datetime.combine(today, item["ended_at"], tzinfo=MOSCOW_TZ)
        auto_finish_dt = event_end_dt + timedelta(minutes=30)

        finished_auto = now_dt >= auto_finish_dt

        # Финальный статус завершения
        finished = finished_manually or finished_auto

        item["is_finished"] = finished

    # Теперь определяем, какой доклад активен
    now_dt = now_moscow()
    previous_all_finished = True
    active_assigned = False

    for idx, item in enumerate(program):
        # базовый статус
        item["is_active"] = False

        # если уже нашли активный — остальные не активны
        if active_assigned:
            continue

        # если какой-то предыдущий доклад не завершен,
        # следующие не могут стать активными
        if not previous_all_finished:
            continue

        # если текущий доклад уже завершен — просто идём дальше
        if item["is_finished"]:
            continue

        # проверяем, началось ли время доклада по расписанию
        start_dt = datetime.combine(today, item["started_at"], tzinfo=MOSCOW_TZ)
        if now_dt >= start_dt:
            # это первый НЕ завершённый доклад, время которого уже наступило
            item["is_active"] = True
            active_assigned = True

        # если доклад не завершен — все последующие считаются "после незавершенного"
        if not item["is_finished"]:
            previous_all_finished = False

    return program


# ЛОГИКА ДЛЯ КНОПКИ СПИКЕРА
def finish_current_talk_for_speaker(speaker_username: str):
    """
    Ищет активный доклад для данного спикера и помечает его завершённым.

    speaker_username — username телеграма БЕЗ '@' или С '@' (обрабатываем оба случая).

    Возвращает (event, session) если что-то нашлось,
    иначе (None, None).
    """
    if not speaker_username:
        return None, None

    username_norm = speaker_username.lstrip("@").lower()

    events = get_today_events()

    for event in events:
        event_id = event["id"]
        program = get_event_program(event_id)

        for idx, session in enumerate(program):
            prog_username = (session.get("speaker_username") or "").lstrip("@").lower()

            # должен совпасть username И доклад должен быть активным
            if prog_username == username_norm and session.get("is_active"):
                # помечаем доклад завершённым
                mark_session_finished(event_id, idx)

                # возвращаем актуальные данные по этому докладу
                updated_program = get_event_program(event_id)
                updated_session = updated_program[idx]
                return event, updated_session

    return None, None
