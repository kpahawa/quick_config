import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


ENV_VARS = {
    "DATABASE_ACCESS": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    "VAR1": {
        "VAR2": {
            "VAR3": "some_value"
        }
    },
    "my_list": [
        "first",
        "second",
    ]
}
