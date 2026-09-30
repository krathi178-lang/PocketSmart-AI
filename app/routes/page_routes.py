from fastapi import APIRouter,Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..auth import current_user
from ..database import get_db
r=APIRouter(); t=Jinja2Templates(directory='app/templates')
def ctx(req,user=None,**kw):return {'request':req,'user':user,**kw}
@r.get('/')
def index(request:Request):return t.TemplateResponse('index.html',ctx(request))
@r.get('/login')
def login(request:Request):return t.TemplateResponse('login.html',ctx(request))
@r.get('/register')
def register(request:Request):return t.TemplateResponse('register.html',ctx(request))
def protected(request,page,**kw):
    try:u=current_user(request)
    except Exception:return RedirectResponse('/login',303)
    return t.TemplateResponse(page,ctx(request,u,**kw))
@r.get('/dashboard')
def dashboard(request:Request):
    try:u=current_user(request)
    except Exception:return RedirectResponse('/login',303)
    with get_db() as db:rows=db.execute('SELECT id,planner_type,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC LIMIT 5',(u['id'],)).fetchall()
    return t.TemplateResponse('dashboard.html',ctx(request,u,recent=rows))
@r.get('/planner/home')
def hp(request:Request):return protected(request,'home_planner.html')
@r.get('/planner/party')
def pp(request:Request):return protected(request,'party_planner.html')
@r.get('/planner/jewelry')
def jp(request:Request):return protected(request,'jewelry_planner.html')
@r.get('/history')
def hist(request:Request):
    try:u=current_user(request)
    except Exception:return RedirectResponse('/login',303)
    with get_db() as db:rows=db.execute('SELECT * FROM recommendations WHERE user_id=? ORDER BY id DESC',(u['id'],)).fetchall()
    return t.TemplateResponse('history.html',ctx(request,u,rows=rows))
