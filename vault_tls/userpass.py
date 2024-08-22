import hvac
import hvac.exceptions
import os
import urllib3
from kv2 import create_secret, read_secret
from init_vault import health_check, create_acl_policy, enable_auth_method
from hvac.api.auth_methods.userpass import Userpass


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


APP = hvac.Client(url='https://localhost:9200', verify=False, token=os.environ.get('VAULT_TOKEN'))


# Userpass method similar to basic authentication with login and password
username = 'test'
password = '123'

secret_name = 'key'
secret_to_vault = 'Qwerty'

policy = {
        'name': 'kv-read-policy',
        'policy': 'path "secret/*" { capabilities = [ "create", "read", "update", "list" ]}',
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
def create_user_userpass(userpass_creds):
    print("[start] Creating user for userpass authentication")
    try:
        Userpass.create_or_update_user(APP, 
                                   username=userpass_creds['username'], 
                                   password=userpass_creds['password'], 
                                   policies=userpass_creds['policies'])
        print(f"[+] New user '{userpass_creds['username']}' created with policy '{userpass_creds['policies'][0]}'")
    except Exception as e:
        print(f"[-] Error creating user: {e}")

create_user_userpass(userpass_creds)

# Step 4: Login via userpass and get token
# Docs: https://hvac.readthedocs.io/en/stable/source/hvac_api_auth_methods.html
def userpass_login(username, password):
    '''Функция выполняет логин в хранилище по логину и паролю метод userpass. Возвращает токен hvs.<...>'''
    try: 
        client_token_raw = APP.auth.userpass.login(
        username=username,
        password=password)
        client_token = client_token_raw['auth']['client_token'] # парсим токен и получает только его значение
        print(f"[+] Successfully get token: {client_token} with policies: {client_token_raw['auth']['token_policies']}")
        return client_token
    except hvac.exceptions.InvalidRequest:
        print("[-] Invalid username or password")
        return None
    except hvac.exceptions.InvalidPath:
        print("[-] Invalid path")
        return None

userpass_token = userpass_login(username, password)

# Step 5: Create secret
create_secret(userpass_token, secret_path='/v1/kv/data/', secret_name = 'test_value_name', secret_to_vault = 'Qwerty123')

# Step 6: Read secret from vault
read_secret(userpass_token, path='v1')