import hvac
import hvac.exceptions
import os
from hvac.api.auth_methods.approle import AppRole
from init_vault import health_check, create_acl_policy, enable_auth_method
from kv2 import create_secret, read_secret

APP = hvac.Client(url=os.environ.get("VAULT_URL"), verify=False, token=os.environ.get("VAULT_TOKEN"))


# Approle method like ................
# https://hvac.readthedocs.io/en/stable/usage/auth_methods/approle.html

# ENV
policy = {
        'name': 'kv-read-policy',
        'policy': 'path "kv/*" { capabilities = [ "create", "read", "update", "list" ]}',
    }

auth_method = {
    "method_type": 'approle',
    "description": 'Enable approle authentification',
    "path": 'approle'
}

approle_creds = {
        "role_name": "test_approle",
        "policies": ["kv-read-policy"],
        "mount_point": "approle"
    }


# Step 0: Helthcheck
health_check()

# Step 1. Create ACL Policy
create_acl_policy(policy)

# Step 2: Enable Approle authentication
enable_auth_method(auth_method)

# Step 3: Create a role with policy attached 
# CLI: vault read auth/approle/role/test_approle
def create_role():
    creds = approle_creds
    AppRole.create_or_update_approle(APP, 
                                    role_name=creds['role_name'],
                                    token_policies=creds['policies'])
    print(f"[+] New role '{creds['role_name']}' created with policy '{creds['policies'][0]}'")
    try: 
        result = AppRole.list_roles(APP, mount_point='approle')
        print(f'[info] the role {result['data']['keys']} was created before')
    except hvac.exceptions.InvalidPath:
        print("[-] no role found")
        
create_role()


# Step 4: Get RoleID
# Хорошая практика это доставка RoleID через trusted provider (k8s, jenkins, etc.). в данном случае мы напрямую мы обращаемся минуя провайдера
def get_role_id():
    creds = approle_creds
    role_id = AppRole.read_role_id(APP, role_name=creds['role_name'], mount_point=creds['mount_point'])
    print(f'[+] Success: role id {role_id['data']['role_id']}')
    return role_id['data']['role_id']
role_id = get_role_id()

# Step 5: Request for wrapped Secret_ID
# Хорошая практика это доставка Secret_ID через trusted provider (k8s, jenkins, etc.). в данном случае мы напрямую мы обращаемся минуя провайдера
def generate_wrapped_secret_id():
    creds = approle_creds
    wrapped_secret = AppRole.generate_secret_id(APP, creds['role_name'], 
                               metadata=None, 
                               cidr_list=None, 
                               token_bound_cidrs=None, 
                               mount_point=creds['mount_point'], 
                               wrap_ttl='5m')
    # Unwrap the token
    # unwrapped_token = APP.auth.unwrap_token(secret_id['data']['accessor'])

    print(f'[+] Success: accessor for wrapped secret id {wrapped_secret['wrap_info']['accessor']}')
    return wrapped_secret['wrap_info']['token']

wrapped_secret = generate_wrapped_secret_id()


# Step 6: Unwrapped Secret
def get_unwrap_secret(wrapped_secret):
    unwrap_response = APP.sys.unwrap(token=wrapped_secret)
    print(f'[+] Success: unwrapped secret {unwrap_response['data']['secret_id']}')
    return unwrap_response['data']['secret_id']

unwrap_secret = get_unwrap_secret(wrapped_secret)

# Step 7: Login with RoleID & SecretID
def approle_login(role_id, secret_id):
    '''Функция выполняет логин в хранилище метод AppRole. Возвращает токен hvs.<...>'''
    try: 
        client_token_raw = APP.auth.approle.login(role_id=role_id, secret_id=secret_id)
        client_token = client_token_raw['auth']['client_token'] # парсим токен и получает только его значение
        print(f"[+] Successfully get token: {client_token[:30]}... with policies: {client_token_raw['auth']['token_policies']}")
        APP.token = client_token
        return APP.token
    except hvac.exceptions.InvalidRequest:
        print("[-] Invalid username or password")
        return None
    except hvac.exceptions.InvalidPath:
        print("[-] Invalid path")
        return None

token = approle_login(role_id, unwrap_secret)

# Step 8: Create secret
create_secret(token, secret_path='v1', secret_name = 'DEMO_APPROLE_WRAPPED', secret_to_vault = 'DEMO_SECRET')

# Step 9: Read secret from vault
read_secret(token, path='v1')