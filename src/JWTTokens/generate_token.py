import jwt
import datetime
from src.config import SECRET_KEY

def generate_token(email,role_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': email,
            'role_id': int(role_id)
        }
        token = jwt.encode(payload, SECRET_KEY['secret_key'], algorithm='HS256')
        # return token.decode('utf-8')
        return token
    except Exception as e:
        return str(e)
