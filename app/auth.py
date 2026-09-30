from fastapi import Request,HTTPException
from .database import get_db
from .utils import decode_token

def current_user(request:Request):
    uid=decode_token(request.cookies.get('pocketsmart_token',''))
    if not uid: raise HTTPException(401,'Login required')
    with get_db() as db: row=db.execute('SELECT id,name,email FROM users WHERE id=?',(uid,)).fetchone()
    if not row: raise HTTPException(401,'User not found')
    return dict(row)
