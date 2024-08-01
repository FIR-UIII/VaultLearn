import hvac
APP = hvac.Client()


def create_secret(token, secret_path, secret_name, secret_to_vault):
    try:
        APP.token = token
        print(f'[info] trying create secret {secret_name} with token {APP.token} to {secret_path}')
        APP.secrets.kv.v2.create_or_update_secret(
                                path=secret_path,
                                secret=dict(secret_name = secret_to_vault))   
        print('[+] Secret created')
    except hvac.exceptions.InvalidPath:
        print("[-] Invalid path")
        return None
    except hvac.exceptions.Forbidden:
        print("[-] Permission denied")
        return None

def read_secret(token, path):
    try:
        APP.token = token
        secret = APP.secrets.kv.v2.read_secret(path=path)   
        secret_value = secret['data']['data']['secret_name']
        print(f'[+] Secret is: path "{path}": value is "{secret_value}"')
    except hvac.exceptions.InvalidPath:
        print("[-] Invalid path")
        return None
    