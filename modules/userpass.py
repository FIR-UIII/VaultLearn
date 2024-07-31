import hvac
import hvac.exceptions
from init_vault import create_acl_policy, enable_userpass_auth, create_user_userpass

APP = hvac.Client()
APP.token = 'test'

# вызвать текущий токен можно через APP.token там же можно его переназначить

username = 'test'
password = '123'

secret_name = 'key'
secret_to_vault = 'Qwerty'

# Step 0: initialize the vault and create user with policy
create_acl_policy()
enable_userpass_auth()
create_user_userpass()


# Step 1 - Login with creds at vault and get token
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

userpass_token = userpass_login(username, password)

# Step 2 - Login with creds at vault and create secret
# Путь всегда уникален. Один путь один секрет ключ:значение
def create_secret():
    APP.secrets.kv.v2.create_or_update_secret(
    path='mykey/v1',
    secret=dict(secret_name=secret_to_vault))   
    print('[+] Secret created')

create_secret()

# Step 3 - Read secret from vault
def read_secret():
    path='mykey/v1'
    secret = APP.secrets.kv.v2.read_secret(
    path=path,
)   
    secret_value = secret['data']['data']['secret_name']
    print(f'[+] For path "{path}": secret value is "{secret_value}"')
    
read_secret()