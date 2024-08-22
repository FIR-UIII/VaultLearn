import hvac
import urllib3
import os

urllib3.disable_warnings() # disable warnings in logs - need to clear

APP = hvac.Client(url=os.environ.get("VAULT_URL"), verify=False, token=os.environ.get("VAULT_TOKEN"))


def create_secret(token, secret_path, secret_name, secret_to_vault):
    try:
        APP.token = token
        print(f'[info] trying create secret {secret_name} with token {APP.token[:30]}... to {secret_path}')
        APP.secrets.kv.v2.create_or_update_secret(
                                path=secret_path,
                                secret=dict(secret_name = secret_to_vault),
                                mount_point='kv')   
        print('[+] Secret created')
    except Exception as e:
        print(f"[-] {e}")
        return None
    except hvac.exceptions.Forbidden:
        print("[-] Permission denied")
        return None

def read_secret(token, path):
    try:
        APP.token = token
        secret = APP.secrets.kv.v2.read_secret(path=path, mount_point='kv')   
        secret_value = secret['data']['data']['secret_name']
        print(f'[+] Secret is: path "{path}": value is "{secret_value}"')
    except Exception as e:
        print(f"[-] {e}")
    