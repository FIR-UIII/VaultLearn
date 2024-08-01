import hvac
import time
import hvac.exceptions


APP = hvac.Client(url="http://127.0.0.1:8200")
APP.token = 'test'


# docs: https://hvac.readthedocs.io/en/stable/usage/
# Step 0: healthcheck of the vault
def check_vault_status():
    print('[info] Checking vault availability')
    status = APP.sys.read_seal_status()
    init_status = status['initialized']
    sealed_status = status['sealed']
    print(f'[info] vault is running: {init_status} \n[info] vault sealed: {sealed_status}')
    if init_status is True  and sealed_status is False:
        print('[+] vault is ready')
        return True
    else:
        print('[-] vault is not ready')
        return False

def health_check():
    for _ in range(5):
        if check_vault_status():
            break
        time.sleep(1)

# Step 1. Create ACL Policy
def create_acl_policy(policy):
    result = APP.sys.list_acl_policies()
    result = result['data']['keys']
    # Check if the policy exists already. If it does, print the current policies. Else, create a new one.
    if 'kv-read-policy' in result:
        return print(f"[+] active policies: {result}")
    else:
    # Create a new ACL policy with read capabilities for the path "secret/*"
        APP.sys.create_or_update_acl_policy(
        name=policy['name'], policy=policy['policy'])
        return print(f"[+] policy '{policy['name']}' has been activated")
    

# Step 2. Enable auth method
def enable_auth_method(auth_method):
    # Check if the auth method exists already. If it does, print the current methods. Else, create a new one.
    list_auth_methods = APP.sys.list_auth_methods()
    if 'token/' in list_auth_methods:
        print(f"[+] token auth enable")
    if 'userpass/' in list_auth_methods:
        print(f"[+] userpass auth enable")
    else:
        APP.sys.enable_auth_method(
            method_type=auth_method['method_type'],
            description=auth_method['description'],
            path=auth_method['path'],
            )
        print(f'[+] {auth_method['method_type']} created and enabled')