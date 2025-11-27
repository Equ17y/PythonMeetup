from datetime import datetime, time

# Временные данные мероприятий (позже заменим на БД)
def get_today_events():
    """
    Возвращает список сегодняшних мероприятий
    """
    today = datetime.now().date()
    
    events = [
        {
            'id': 1,
            'name': 'Тема мероприятия #1',
            'event_date': today,
            'started_at': time(10, 0),
            'ended_at': time(13, 0),
            'is_active': False,
        },
        {
            'id': 2,
            'name': 'Тема мероприятия #2',
            'event_date': today,
            'started_at': time(13, 0),
            'ended_at': time(16, 0),
            'is_active': True,
        },
        {
            'id': 1,
            'name': 'Тема мероприятия #3',
            'event_date': today,
            'started_at': time(16, 0),
            'ended_at': time(19, 0),
            'is_active': False,
        }
    ]
    
    return events

def get_event_program(event_id):
    """
    Возвращает программу конкретного мероприятия
    """
    programs = {
        1: [
            {
                'started_at': time(10, 0),
                'ended_at': time(11, 0),
                'topic': 'Тема доклада #1',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            },
            {
                'started_at': time(11, 0),
                'ended_at': time(12, 0),
                'topic': 'Тема доклада #2',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            },
            {
                'started_at': time(12, 0),
                'ended_at': time(13, 0),
                'topic': 'Тема доклада #3',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            }
        ],
        2: [
            {
                'started_at': time(13, 0),
                'ended_at': time(14, 0),
                'topic': 'Тема доклада #1',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': True
            },
            {
                'started_at': time(14, 0),
                'ended_at': time(15, 0),
                'topic': 'Тема доклада #2',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            },
            {
                'started_at': time(15, 0),
                'ended_at': time(16, 0),
                'topic': 'Тема доклада #3',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            }
        ],
        3: [
            {
                'started_at': time(16, 0),
                'ended_at': time(17, 0),
                'topic': 'Тема доклада #1',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            },
            {
                'started_at': time(17, 0),
                'ended_at': time(18, 0),
                'topic': 'Тема доклада #2',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            },
            {
                'started_at': time(18, 0),
                'ended_at': time(19, 0),
                'topic': 'Тема доклада #3',
                'speaker': 'Иван Петров',
                'speaker_username': '@rakhimzhanovamir',
                'is_active': False
            }
        ]
    }
    
    return programs.get(event_id, [])