import os
from channels.layers import get_channel_layer

try:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'portfolio',
            'PASSWORD':'Racer1525$',
            'USER':'john',
            'HOST':'localhost',
            'PORT':'5432',
        }
    }
except DatabaseError:
    pass


ASGI_APPLICATION = 'dating_app.asgi.application'

# Configure Channel Layers using Redis
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')],
        },
    },
}

from dotenv import load_dotenv

load_dotenv()


EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)


#paypal LOGIC

PAYPAL_CLIENT_ID = 'your-paypal-client-id'
PAYPAL_CLIENT_SECRET = 'your-paypal-client-secret'

#Mpesa
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
MPESA_ENVIRONMENT = 'sandbox'

#Pesapal
PESAPAL_DEMO = True  # Set to False for production

PESAPAL_CONSUMER_KEY = 'd9adGJMrebaNden8xiTo7UzMOKLpTi3R'
PESAPAL_CONSUMER_SECRET = 'vwQjT4dQ53jLSo5+1fh5ZFUPk/Y='

PESAPAL_IFRAME_LINK = 'http://demo.pesapal.com/api/PostPesapalDirectOrderV4' if PESAPAL_DEMO else 'https://www.pesapal.com/api/PostPesapalDirectOrderV4'
PESAPAL_QUERY_STATUS_LINK = 'http://demo.pesapal.com/API/QueryPaymentDetails' if PESAPAL_DEMO else 'https://www.pesapal.com/API/QueryPaymentDetails'

PESAPAL_OAUTH_CALLBACK_URL = 'transaction_completed'
PESAPAL_OAUTH_SIGNATURE_METHOD = 'SignatureMethod_HMAC_SHA1'

PESAPAL_TRANSACTION_DEFAULT_REDIRECT_URL = 'after_login'  # Adjust as needed
PESAPAL_TRANSACTION_FAILED_REDIRECT_URL = 'after_login'
PESAPAL_REDIRECT_WITH_REFERENCE = True
PESAPAL_TRANSACTION_MODEL = 'django_pesapal.Transaction'



#Flutter Wave
FLUTTERWAVE_SECRET_KEY = '<your-flutterwave-secret-key>'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_REDIRECT_URL = 'after_login'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


#CRF Token valivador
CSFR_TRUSTED_ORIGINS=[
    'https://eea7-105-161-98-8.ngrok-free.app'
]
