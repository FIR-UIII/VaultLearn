import hvac
import hvac.exceptions
from init_vault import initialize_vault

APP = hvac.Client()
APP.token = 'test'

# Approle method like ................
# https://hvac.readthedocs.io/en/stable/usage/auth_methods/approle.html

# Enable Approle
APP.sys.enable_auth_method(
    method_type='approle',
)

# Mount approle auth method under a different path:
APP.sys.enable_auth_method(
    method_type='approle',
    path='my-approle',
)

# Authentication


# Create or Update AppRole