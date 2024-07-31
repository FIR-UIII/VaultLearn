import hvac
import hvac.exceptions
from hvac.api.auth_methods.userpass import Userpass


APP = hvac.Client(url="http://127.0.0.1:8200")


# Step 1. Create ACL Policy
def create_acl_policy():
    APP.token = 'test'
    result = APP.sys.list_acl_policies()
    result = result['data']['keys']
    # Check if the policy exists already. If it does, print the current policies. Else, create a new one.
    if 'kv-read-policy' in result:
        return print(f"[+] active policies: {result}")
    else:
    # Create a new ACL policy with read capabilities for the path "secret/*"
        APP.sys.create_or_update_acl_policy(
        name="kv-read-policy", policy='path "secret/*" { capabilities = [ "create", "read", "update", "list" ]}',
    )


# Step 2. Enable userpass auth method
def enable_userpass_auth():
    APP.token = 'test'
    # Check if the userpass auth method is enabled. If it is, print a message. Else, enable it.
    try:
        print('[ info ] Check if userpass auth is enabled')
        response = APP.sys.read_auth_method_tuning(path='userpass')
        response = response['data']

    # Check if the userpass auth method is enabled. If it is, print a message. Else, enable it.
        if response:
            print(f'[+] The userpass auth method is enable')            
        else:
            print(f'[-] The userpass auth method is NOT enable')
            print(f'[+] Creating userpass auth method')
            APP.sys.enable_auth_method(
                method_type='userpass',
                description='Enable userpass authentification',
                path='userpass',
                )
    except hvac.exceptions.InvalidRequest:
        print(f'[-] The userpass auth method is NOT enable')
        print(f'[*] Creating userpass auth method is NOT enable')
        APP.sys.enable_auth_method(
        method_type='userpass',
            description='Enable userpass authentification',
            path='userpass',
        )

# Step 3. Create user for userpass auth method userpass and policy kv-read-policy
def create_user_userpass():
    creds = {
        "username": "test",
        "password": "123",
        "policies": ["kv-read-policy"],
    }

    Userpass.create_or_update_user(APP, username=creds['username'], password=creds['password'], policies=creds['policies'])
    print(f"[+] New user '{creds['username']}' created with policy '{creds['policies'][0]}'")