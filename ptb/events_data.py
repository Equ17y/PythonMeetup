from datetime import datetime
from zoneinfo import ZoneInfo
from meetup_core.models import Event, SpeakerTopic

# Часовой пояс Москвы
MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def now_moscow() -> datetime:
    """Возвращает текущее московское время."""
    return datetime.now(MOSCOW_TZ)


def get_today_events():
    """
    Возвращает список сегодняшних мероприятий с полем is_active,
    которое определяется по программе докладов.
    """
    today = now_moscow().date()
    events_db = Event.objects.filter(event_date=today)

    events = []
    for event in events_db:
        program = get_event_program(event.id)
        event_is_active = any(s.get("is_active") for s in program)

        events.append({
            "id": event.id,
            "name": event.name,
            "event_date": event.event_date,
            "started_at": event.started_at,
            "ended_at": event.ended_at,
            "is_active": event_is_active,
        })

    return events


def get_event_program(event_id):
    """
    Возвращает программу мероприятия с двумя статусами:
    - is_finished: завершён ли доклад (по времени)
    - is_active: доклад, который «идёт сейчас»
    """
    now_dt = now_moscow()
    today = now_dt.date()

    sessions_db = SpeakerTopic.objects.filter(
        event_id=event_id
    ).select_related('speaker').order_by('started_at')

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

    # Логика определения статусов
    current_active_index = -1

    for idx, (item, session_obj) in enumerate(zip(program, sessions_db)):
        # Рассчитываем время начала и окончания
        start_dt = datetime.combine(today, session_obj.started_at, tzinfo=MOSCOW_TZ)
        end_dt = datetime.combine(today, session_obj.ended_at, tzinfo=MOSCOW_TZ)

        # Доклад завершен?
        item["is_finished"] = now_dt > end_dt

        # Доклад активен?
        item["is_active"] = start_dt <= now_dt <= end_dt

        if item["is_active"]:
            current_active_index = idx

    # Если есть активный доклад, остальные не могут быть активными
    if current_active_index >= 0:
        for idx, item in enumerate(program):
            if idx != current_active_index:
                item["is_active"] = False

    return program


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
            'is_active': False,  # Будущие мероприятия никогда не активны
        })

    return events


def get_next_event_program(event_id):
    """
    Возвращает программу конкретного мероприятия (следующего)
    """
    sessions_db = SpeakerTopic.objects.filter(
        event_id=event_id
    ).select_related('speaker').order_by('started_at')

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
            'is_active': False,
            'is_finished': False,
        })

    return program
