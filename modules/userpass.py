import hvac
import hvac.exceptions
import os
from secret_engine.kv2 import create_secret, read_secret
from init_vault import health_check, create_acl_policy, enable_auth_method
from hvac.api.auth_methods.userpass import Userpass
import urllib3

urllib3.disable_warnings() # disable warnings in logs - need to clear


APP = hvac.Client(url=os.environ.get("VAULT_URL"), verify=False, token=os.environ.get("VAULT_TOKEN"))


# Userpass method similar to basic authentication with login and password
username = 'test'
password = '123'

secret_name = 'demo_key'
secret_to_vault = 'DEMO_SECRET'

policy = {
        'name': 'kv-read-policy',
        'policy': 'path "kv/*" { capabilities = [ "create", "read", "update", "list" ]}',
    }

auth_method = {
    "method_type": 'userpass',
    "description": 'Enable userpass authentification',
    "path": 'userpass'
}

userpass_creds = {
        "username": "test",
        "password": "123",
        "policies": ["kv-read-policy"],
    }


# Step 0: healthcheck the vault and init for userpass authentication
health_check()

# Step 1: Create ACL Policy
create_acl_policy(policy)

# Step 2: Enable userpass auth method
enable_auth_method(auth_method)

# Step 3 - Create user for userpass auth add ACL policy
def create_user_userpass():
    creds = userpass_creds
    Userpass.create_or_update_user(APP, 
                                   username=creds['username'], 
                                   password=creds['password'], 
                                   policies=creds['policies'])
    print(f"[+] New user '{creds['username']}' created with policy '{creds['policies'][0]}'")

create_user_userpass()

# Step 4: Login via userpass and get token
# Docs: https://hvac.readthedocs.io/en/stable/source/hvac_api_auth_methods.html
def userpass_login(username, password):
    '''Функция выполняет логин в хранилище по логину и паролю метод userpass. Возвращает токен hvs.<...>'''
    try: 
        client_token_raw = APP.auth.userpass.login(
        username=username,
        password=password)
        client_token = client_token_raw['auth']['client_token'] # парсим токен и получает только его значение
        print(f"[+] Successfully get token: {client_token[:30]}... with policies: {client_token_raw['auth']['token_policies']}")
        return client_token
    except hvac.exceptions.InvalidRequest:
        print("[-] Invalid username or password")
        return None
    except hvac.exceptions.InvalidPath:
        print("[-] Invalid path")
        return None

userpass_token = userpass_login(username, password)

# Step 5: Create secret
create_secret(userpass_token, secret_path='kv', secret_name = 'test_value_name', secret_to_vault = 'Qwerty123')

# Step 6: Read secret from vault
read_secret(userpass_token, path='kv')