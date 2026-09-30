from fastapi import APIRouter,Form
from fastapi.responses import RedirectResponse,JSONResponse
from ..database import get_db
from ..utils import hash_password,verify_password,create_token
from ..config import SESSION_COOKIE,COOKIE_SECURE
r=APIRouter()
@r.post('/register')
async def register(name:str=Form(...),email:str=Form(...),password:str=Form(...)):
    email=email.strip().lower()
    if len(name.strip())<2 or len(password)<6:return JSONResponse({'error':'Name must be 2+ chars and password 6+ chars.'},422)
    with get_db() as db:
        if db.execute('SELECT id FROM users WHERE email=?',(email,)).fetchone():return JSONResponse({'error':'Email already registered.'},409)
        uid=db.execute('INSERT INTO users(name,email,password_hash) VALUES(?,?,?)',(name.strip(),email,hash_password(password))).lastrowid
    x=RedirectResponse('/dashboard',303); x.set_cookie(SESSION_COOKIE,create_token(uid),httponly=True,samesite='lax',secure=COOKIE_SECURE,max_age=86400); return x
@r.post('/login')
async def login(email:str=Form(...),password:str=Form(...)):
    with get_db() as db: row=db.execute('SELECT * FROM users WHERE email=?',(email.strip().lower(),)).fetchone()
    if not row or not verify_password(password,row['password_hash']):return JSONResponse({'error':'Invalid email or password.'},401)
    x=RedirectResponse('/dashboard',303); x.set_cookie(SESSION_COOKIE,create_token(row['id']),httponly=True,samesite='lax',secure=COOKIE_SECURE,max_age=86400); return x
@r.get('/logout')
def logout():
    x=RedirectResponse('/',303); x.delete_cookie(SESSION_COOKIE); return x
@r.post('/token')
async def token(email:str=Form(...),password:str=Form(...)):
    with get_db() as db: row=db.execute('SELECT * FROM users WHERE email=?',(email.strip().lower(),)).fetchone()
    if not row or not verify_password(password,row['password_hash']):return JSONResponse({'error':'Invalid credentials'},401)
    return {'access_token':create_token(row['id']),'token_type':'bearer'}
