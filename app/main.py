from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .config import APP_NAME
from .database import init_db
from .routes import page_routes,auth_routes,planner_routes
app=FastAPI(title=APP_NAME,version='1.0.0',description='GenAI budget recommendation assistant')
app.add_middleware(CORSMiddleware,allow_origins=['http://127.0.0.1:8000','http://localhost:8000'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
app.mount('/static',StaticFiles(directory='app/static'),name='static')
app.include_router(page_routes.r);app.include_router(auth_routes.r);app.include_router(planner_routes.r)
@app.on_event('startup')
async def startup():init_db()
@app.get('/health')
def health():from .gemini_service import service;return {'status':'ok','gemini_configured':bool(service.client)}
