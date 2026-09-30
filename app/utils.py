import base64,hashlib,hmac,secrets
from datetime import datetime,timedelta,timezone
from jose import jwt
from .config import SECRET_KEY,JWT_ALGORITHM

def hash_password(password):
    salt=secrets.token_bytes(16); d=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,210000)
    return f"pbkdf2_sha256$210000${base64.urlsafe_b64encode(salt).decode()}${base64.urlsafe_b64encode(d).decode()}"
def verify_password(password,stored):
    try:
        scheme,rounds,salt,digest=stored.split('$'); s=base64.urlsafe_b64decode(salt); expected=base64.urlsafe_b64decode(digest)
        return scheme=='pbkdf2_sha256' and hmac.compare_digest(hashlib.pbkdf2_hmac('sha256',password.encode(),s,int(rounds)),expected)
    except Exception:return False
def create_token(user_id):
    exp=datetime.now(timezone.utc)+timedelta(hours=24)
    return jwt.encode({'sub':str(user_id),'exp':exp},SECRET_KEY,algorithm=JWT_ALGORITHM)
def decode_token(token):
    try:return int(jwt.decode(token,SECRET_KEY,algorithms=[JWT_ALGORITHM])['sub'])
    except Exception:return None
