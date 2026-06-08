from os import environ

SESSION_CONFIGS = [
    dict(
        name='Main',
        app_sequence=[
            'intro',
            's1',
        ],
        num_demo_participants=10,
        completionlinkfull='https://app.prolific.com/submissions/complete?cc=C1PO8E12',
    )
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

ROOMS = [
    dict(
        name='prolific_main',
        display_name='Main Experiment Room',
        # participant_label_file='_rooms/prolific_main.txt',  # optional: for fixed labels
        # use_secure_urls=True,  # optional: adds participant-specific tokens
    ),
]

PARTICIPANT_FIELDS = ['s1score']
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '7127299695462'

OTREE_PRODUCTION = environ.get('OTREE_PRODUCTION', '0') == '1'
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL', '')