import json
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from ..auth import current_user
from ..database import get_db
from ..gemini_service import service
from ..schemas import Home, Party
from ..catalog import catalog

r = APIRouter()

def save(uid, kind, data, out):
    with get_db() as db:
        return db.execute(
            "INSERT INTO recommendations(user_id,planner_type,request_json,response_json) VALUES(?,?,?,?,?)",
            (uid, kind, json.dumps(data), json.dumps(out))
        ).lastrowid

def safe_generate(kind, data, image=None, mime=None):
    try:
        return service.generate(kind, data, image, mime)
    except Exception as e:
        print(f"{kind.upper()} GENERATION ERROR:", repr(e))
        return service.fallback(kind, data, catalog(kind), bool(image))

@r.post('/generate-home')
async def home(p: Home, request: Request):
    u = current_user(request)
    d = p.model_dump()
    out = safe_generate('home', d)
    try: i = save(u['id'], 'home', d, out)
    except Exception as e: print('HOME SAVE ERROR:', repr(e)); i = 0
    return {'id': i, 'planner_type': 'home', 'source': 'gemini' if service.client else 'demo-fallback', **out}

@r.post('/generate-party')
async def party(p: Party, request: Request):
    u = current_user(request)
    d = p.model_dump()
    out = safe_generate('party', d)
    try: i = save(u['id'], 'party', d, out)
    except Exception as e: print('PARTY SAVE ERROR:', repr(e)); i = 0
    return {'id': i, 'planner_type': 'party', 'source': 'gemini' if service.client else 'demo-fallback', **out}

@r.post('/generate-jewelry')
async def jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form('Special Occasion'),
    style: str = Form('Elegant'),
    outfit_description: str = Form(''),
    outfit_image: UploadFile | None = File(None),
):
    u = current_user(request)
    if budget <= 0:
        raise HTTPException(422, 'Budget must be greater than zero.')

    image = None
    mime = None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {'image/jpeg', 'image/png', 'image/webp'}:
            raise HTTPException(415, 'Use JPG, PNG or WEBP.')
        image = await outfit_image.read()
        mime = outfit_image.content_type
        if len(image) > 5 * 1024 * 1024:
            raise HTTPException(413, 'Image must be 5 MB or smaller.')

    d = {
        'budget': budget,
        'occasion': occasion,
        'style': style,
        'outfit_description': outfit_description,
        'has_outfit_image': bool(image),
    }
    out = safe_generate('jewelry', d, image, mime)
    try: i = save(u['id'], 'jewelry', d, out)
    except Exception as e: print('JEWELRY SAVE ERROR:', repr(e)); i = 0
    return {'id': i, 'planner_type': 'jewelry', 'source': 'gemini' if service.client else 'demo-fallback', **out}

@r.get('/history')
def history(request: Request):
    u = current_user(request)
    with get_db() as db:
        return [dict(x) for x in db.execute(
            'SELECT id,planner_type,request_json,response_json,created_at FROM recommendations WHERE user_id=? ORDER BY id DESC',
            (u['id'],)
        ).fetchall()]

@r.get('/session-info')
def session_info(request: Request):
    u = current_user(request)
    return {'logged_in': True, **u}

@r.get('/session-data')
def session_data(request: Request):
    u = current_user(request)
    with get_db() as db:
        n = db.execute('SELECT COUNT(*) n FROM recommendations WHERE user_id=?', (u['id'],)).fetchone()['n']
    return {'user_id': u['id'], 'recommendation_count': n}

@r.get('/recommendations-details/{rid}')
def details(rid: int, request: Request):
    u = current_user(request)
    with get_db() as db:
        x = db.execute('SELECT * FROM recommendations WHERE id=? AND user_id=?', (rid, u['id'])).fetchone()
    if not x:
        raise HTTPException(404, 'Recommendation not found.')
    return {'id': x['id'], 'planner_type': x['planner_type'], 'request': json.loads(x['request_json']), 'response': json.loads(x['response_json']), 'created_at': x['created_at']}
