import jwt
from datetime import timezone
from datetime import datetime
from datetime import timedelta


def load_private_key(filepath):
    with open(filepath, 'r') as file:
        return file.read()


def create_jwt_token():
    private_key = load_private_key('vault_tls/file/private.pem')

    iat = datetime.now(tz=timezone.utc)
    claims = {
        "iss": "main",
        "iat": iat,
        "exp": iat + timedelta(hours=1),
        "nbf": iat,
        "aud": "main",
        "user_mail": "test@example.com",
    }
    token = jwt.encode(claims, private_key, algorithm="RS256")
    return(token)

if __name__ == '__main__':
    create_jwt_token()