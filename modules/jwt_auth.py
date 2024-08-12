import os
import hvac
import jwt
import urllib3
from kv2 import create_secret, read_secret
from init_vault import health_check, create_acl_policy, enable_auth_method

urllib3.disable_warnings() # disable warnings in logs

APP = hvac.Client(url=os.environ.get("VAULT_URL"), verify=False, token=os.environ.get("VAULT_TOKEN"))

# ENV
policy = {
        'name': 'kv-read-policy',
        'policy': 'path "kv/*" { capabilities = [ "create", "read", "update", "list" ]}',
    }

auth_method = {
    "method_type": 'jwt',
    "description": 'Enable JWT authentification',
    "path": 'jwt'
}

jwt_config = {
        "role_name": "demo_jwt",
        "policies": ["kv-read-policy"],
        "mount_point": "jwt"
    }

# Payload for JWT
payload = {
    "sub": "1234567890",
    "name": "John Doe",
    "admin": True
}
key = 'vault'

# Step 0: Helthcheck
health_check()

# Step 1. Create ACL Policy
create_acl_policy(policy)

# Step 2: Enable Approle authentication
enable_auth_method(auth_method)

# Step 3: Create JWT role
def create_jwt_role(jwt_config):
    # Check if role is already defined
    # read_response = APP.auth.jwt.list_roles(path='jwt/')
    # if read_response['data']['keys'] is not None:
    #     print('[info] Role already defined. Skipping creating role')
    #     return None
    # else:
        try:
            print('[info] Creating role for JWT authentification')
            APP.auth.jwt.create_role(
                                    name=jwt_config['role_name'],
                                    role_type='jwt',
                                    user_claim='sub',
                                    bound_audiences=['12345'],
                                )
            print(f'[+] Success: {jwt_config['role_name']} is enabled')
        except Exception as e:
            print (f'[-] Raise error: {e}')


create_jwt_role(jwt_config)

# Step 4: Create-Get JWT token
def encode_jwt(key, payload):
    encoded = jwt.encode(payload, key, algorithm="HS256")
    print("[+] Success: created JWT:", encoded)
    return encoded

jwt_token = encode_jwt(key, payload)

# Step 5: Login with JWT
def jwt_login(jwt_config):
    print('[info] Trying to login')
    response = APP.auth.jwt.jwt_login(
                                    role=jwt_config['role_name'],
                                    jwt=jwt_token,
                                    use_token=True, 
                                    path='jwt/'
                                )
    print('Client token returned: %s' % response['auth']['client_token'])


jwt_login(jwt_config)

# Step 6: Create secret
# create_secret(token, secret_path='v1', secret_name = 'DEMO_APPROLE', secret_to_vault = 'DEMO_SECRET')

# Step 7: Read secret from vault
# read_secret(token, path='v1')

