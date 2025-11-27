# Временные данные мероприятий (позже заменим на БД)
from datetime import datetime, time
from zoneinfo import ZoneInfo


MOSCOW_TZ = ZoneInfo("Europe/Moscow")


def now_moscow():
    """Возвращает текущее московское время"""
    return datetime.now(MOSCOW_TZ)


def is_active_now(event_date, start_time, end_time):
    """
    Проверяет, идет ли событие или доклад прямо сейчас.
    """

    start_dt = datetime.combine(event_date, start_time, tzinfo=MOSCOW_TZ)
    end_dt = datetime.combine(event_date, end_time, tzinfo=MOSCOW_TZ)

    current = now_moscow()

    return start_dt <= current <= end_dt


def get_today_events():
    """
    Возвращает список сегодняшних мероприятий с автоподсчетом с
    """
    today = now_moscow().date()

    events = [
        {
            'id': 1,
            'name': 'Тема мероприятия #1',
            'event_date': today,
            'started_at': time(0, 0),
            'ended_at': time(13, 0),
        },
        {
            'id': 2,
            'name': 'Тема мероприятия #2',
            'event_date': today,
            'started_at': time(13, 0),
            'ended_at': time(16, 0),
        },
        {
            'id': 3,
            'name': 'Тема мероприятия #3',
            'event_date': today,
            'started_at': time(16, 0),
            'ended_at': time(23, 59),
        }
    ]

    # Вычисляем статус активности
    for event in events:
        event["is_active"] = is_active_now(
            event["event_date"],
            event["started_at"],
            event["ended_at"]
        )

    return events


def get_event_program(event_id):
    """
    Возвращает программу мероприятия с автоподсчетом активности докладов
    """

    programs = {
        1: [
            {
                'started_at': time(0, 0),
                'ended_at': time(11, 0),
                'topic': 'Тема доклада #1',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            },
            {
                'started_at': time(11, 0),
                'ended_at': time(12, 0),
                'topic': 'Тема доклада #2',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            },
            {
                'started_at': time(12, 0),
                'ended_at': time(13, 0),
                'topic': 'Тема доклада #3',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            }
        ],
        2: [
            {
                'started_at': time(13, 0),
                'ended_at': time(14, 0),
                'topic': 'Тема доклада #1',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            },
            {
                'started_at': time(14, 0),
                'ended_at': time(15, 0),
                'topic': 'Тема доклада #2',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            },
            {
                'started_at': time(15, 0),
                'ended_at': time(16, 0),
                'topic': 'Тема доклада #3',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            }
        ],
        3: [
            {
                'started_at': time(16, 0),
                'ended_at': time(17, 0),
                'topic': 'Тема доклада #1',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            },
            {
                'started_at': time(17, 0),
                'ended_at': time(18, 0),
                'topic': 'Тема доклада #2',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            },
            {
                'started_at': time(18, 0),
                'ended_at': time(23, 59),
                'topic': 'Тема доклада #3',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
            }
        ]
    }

    today = now_moscow().date()

    # Вычисляем статус активности
    program = programs.get(event_id, [])
    for item in program:
        item['is_active'] = is_active_now(
            today,
            item['started_at'],
            item['ended_at']
        )

    return program
