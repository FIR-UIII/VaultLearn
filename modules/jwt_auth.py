import os
import hvac
from create_jwt_token import create_jwt_token
from hvac.api.auth_methods.jwt import JWT
import urllib3
from secret_engine.kv2 import create_secret, read_secret
from init_vault import health_check, create_acl_policy, enable_auth_method

urllib3.disable_warnings() # disable warnings in logs

APP = hvac.Client(url=os.environ.get("VAULT_URL"), verify=False, token=os.environ.get("VAULT_TOKEN"))

# ENV
policy = {
        'name': 'kv-read-policy',
        'policy': 'path "kv/*" { capabilities = [ "create", "read", "update", "list" ]}, path "secret/*" { capabilities = [ "create", "read", "update", "list" ]}',
    }

auth_method = {
    "method_type": 'jwt',
    "description": 'Enable JWT authentification',
    "path": 'jwt'
}

jwt_config = {
        "role_name": "demo_jwt",
        "policies": ["kv-read-policy"],
        "mount_point": "jwt",
        "user_claim": "user_mail",
        "allowed_redirect_uris": ['http://localhost:8200'],
        "role_type": "jwt",
        "jwt_validation_pubkeys": "vault_tls/file/pubkey.pem",
        "jwt_supported_algs": ['RS256']
    }

path_to_jwt_pub_cert = 'vault_tls/file/private.pem'

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
                                    role_type=jwt_config['role_type'],
                                    allowed_redirect_uris=jwt_config['allowed_redirect_uris'],
                                    user_claim=jwt_config['user_claim'],
                                    token_policies=jwt_config['policies']
                                )
            print(f'[+] Success: {jwt_config['role_name']} is enabled')
        except Exception as e:
            print (f'[-] Raise error: {e}')


create_jwt_role(jwt_config)

# Step 4: Create JWT configuration
def create_config(jwt_config):
    print('[info] Creating JWT auth configuration')
    '''One (and only one) of oidc_discovery_url and jwt_validation_pubkeys must be set.'''
    try:
        JWT.configure(APP,
                        jwt_validation_pubkeys=jwt_config['jwt_validation_pubkeys'],
                        jwt_supported_algs=jwt_config['jwt_supported_algs'],
                        path=jwt_config['mount_point']
                    )
        print('[+] Success: Creating JWT auth configuration')
    except Exception as e:
         print(f'[-] Raise error: {e}')

create_config(jwt_config)

# Step 5: Create JWT token
jwt_token = create_jwt_token(path_to_jwt_pub_cert)
print(f'[+] Success: created jwt_token: {jwt_token[:30]}...')

# Step 6: Login with JWT
def jwt_login(jwt_config):
    print('[info] Trying to login')
    try:
        response = APP.auth.jwt.jwt_login(
                                    role=jwt_config['role_name'],
                                    jwt=jwt_token,
                                    use_token=True, 
                                    path=jwt_config['mount_point']
                                )
        print('[+] Success: get client token: %s' % response['auth']['client_token'][:30]+"...")
        client_token = response['auth']['client_token']
        return client_token
    except Exception as e:
         print(f'[-] Raise error: {e}')

client_token = jwt_login(jwt_config)

# Step 7: Create secret
create_secret(client_token, secret_path='v1', secret_name = 'DEMO_APPROLE', secret_to_vault = 'DEMO_SECRET')

# Step 8: Read secret from vault
read_secret(client_token, path='v1')