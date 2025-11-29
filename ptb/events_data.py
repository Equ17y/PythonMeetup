from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from meetup_core.models import Event, SpeakerTopic

# Часовой пояс Москвы
MOSCOW_TZ = ZoneInfo("Europe/Moscow")

# Хранилище завершённых докладов:
_FINISHED_SESSIONS: set[tuple[int, int]] = set()


def now_moscow() -> datetime:
    """Возвращает текущее московское время."""
    return datetime.now(MOSCOW_TZ)


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

    events_db = Event.objects.filter(event_date=today)

    events = []
    for event in events_db:
        events.append({
            "id": event.id,
            "name": event.name,
            "event_date": event.event_date,
            "started_at": event.started_at,
            "ended_at": event.ended_at,
        })

    for event in events:
        program = get_event_program(event["id"])
        event["is_active"] = any(s.get("is_active") for s in program)

    return events


def get_event_program(event_id):
    """
    Возвращает программу мероприятия с двумя статусами:
    - is_finished: завершён ли доклад спикером
    - is_active: доклад, который «идёт сейчас»
      (учитывается московское время и завершённость предыдущего доклада)
    """
    now_dt = now_moscow()
    today = now_dt.date()

    sessions_db = SpeakerTopic.objects.filter(event_id=event_id).select_related('speaker').order_by('started_at')

    program = []
    for session in sessions_db:
        speaker_name = session.speaker.name if session.speaker.name else f"Пользователь {session.speaker.tg_id}"
        speaker_username = session.speaker.username if session.speaker.username else f"user_{session.speaker.tg_id}"

        program.append({
            "started_at": session.started_at.strftime('%H:%M'),
            "ended_at": session.ended_at.strftime('%H:%M'),
            "topic": session.topic,
            "speaker": speaker_name,
            "speaker_username": f"@{speaker_username}",
            "speaker_tg_id": session.speaker.tg_id,
        })
    # Сначала проставим is_finished
    for idx, item in enumerate(program):
        # Пометка завершён ли вручную
        finished_manually = is_session_finished(event_id, idx)

        session_obj = sessions_db[idx]

        # Автоматическое завершение через 30 минут после окончания
        event_end_dt = datetime.combine(today, session_obj.ended_at, tzinfo=MOSCOW_TZ)
        auto_finish_dt = event_end_dt + timedelta(minutes=30)

        finished_auto = now_dt >= auto_finish_dt
        # Финальный статус завершения
        finished = finished_manually or finished_auto

        item["is_finished"] = finished

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

        session_obj = sessions_db[idx]
        start_dt = datetime.combine(today, session_obj.started_at, tzinfo=MOSCOW_TZ)
        if now_dt >= start_dt:
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
            # Сравниваем по username (без @)
            prog_username = session['speaker_username'].lstrip("@").lower()
            # должен совпасть username И доклад должен быть активным
            if prog_username == username_norm and session.get("is_active"):
                # помечаем доклад завершённым
                mark_session_finished(event_id, idx)

                # возвращаем актуальные данные по этому докладу
                updated_program = get_event_program(event_id)
                updated_session = updated_program[idx]
                return event, updated_session

    return None, None


def get_next_events():
    """
    Возвращает список следующих мероприятий
    """
    today = now_moscow().date()

    events_db = Event.objects.filter(event_date__gt=today).order_by('event_date')

    events = []
    for event in events_db:
        events.append({
            'id': event.id,
            'name': event.name,
            'event_date': event.event_date,
            'started_at': event.started_at,
            'ended_at': event.ended_at,
            'is_active': event.is_active,
        })

    return events


def get_next_event_program(event_id):
    """
    Возвращает программу конкретного мероприятия (следующего)
    """
    sessions_db = SpeakerTopic.objects.filter(event_id=event_id).select_related('speaker').order_by('started_at')

    program = []
    for session in sessions_db:
        speaker_name = session.speaker.name if session.speaker.name else f"Пользователь {session.speaker.tg_id}"
        speaker_username = session.speaker.username if session.speaker.username else f"user_{session.speaker.tg_id}"

        program.append({
            'started_at': session.started_at.strftime('%H:%M'),
            'ended_at': session.ended_at.strftime('%H:%M'),
            'topic': session.topic,
            'speaker': speaker_name,
            'speaker_username': f"@{speaker_username}",
            'is_active': False
        })

    return program
