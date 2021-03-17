import os


ENV_VARS = {
    "TWILIO_SID": os.environ.get('twilio_sid'),
    "TWILIO_AUTH_TOKEN": os.environ.get('twilio_auth_token'),
    "SECRET_KEY": os.environ.get('secret_key'),
    "IMGUR_KEY": os.environ.get('imgur_key'),
    "ALLOWED_USERS": os.environ.get('allowed_users'),
    "USER_PASSWORD": os.environ.get('user_password'),
    "CUSTOM_AUTH_PREFIX": os.environ.get('custom_auth_prefix'),
}
