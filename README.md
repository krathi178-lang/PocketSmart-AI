# PocketSmart AI — Complete Project

Built from the supplied PocketSmart AI project documentation. The document specifies a FastAPI backend, Gemini multimodal AI, Home/Party/Jewelry planners, authentication, sessions/history, Jinja2 HTML/CSS/JS frontend, and mock/simulated third-party data sources. This implementation includes all of those core components. fileciteturn0file0L35-L49

## What is included
- FastAPI backend with `/generate-home`, `/generate-party`, `/generate-jewelry`
- Registration/login/logout and `/token`
- `/session-info`, `/session-data`, `/history`, recommendation details
- SQLite persistence
- Gemini text + optional image integration
- Mock catalog/search links for Amazon, Flipkart, IKEA, Swiggy, Zomato and OYO
- Responsive Jinja2 frontend
- Home, Party and Jewelry planner pages
- Demo fallback when `GEMINI_API_KEY` is empty
- Smoke tests

## VS Code setup — Windows
1. Extract the ZIP and open the `PocketSmart_AI` folder in VS Code.
2. Open Terminal → New Terminal.
3. Run:
   `py -3.11 -m venv .venv`
4. Activate:
   `\.venv\Scripts\Activate.ps1`
5. Install:
   `pip install -r requirements.txt`
6. Copy `.env.example` to `.env`.
7. Put your Gemini key in `GEMINI_API_KEY` if you want live AI.
8. Start:
   `python -m uvicorn app.main:app --reload`
9. Open `http://127.0.0.1:8000`.

## Gemini model
The course document names Gemini 1.5 Flash Pro. Model names/availability can change, so `GEMINI_MODEL` is configurable. The included default is `gemini-2.5-flash`; if your API account exposes the model specified by your course, put that exact model name in `.env`.

## Demo without an API key
The application still works without a key using deterministic demo recommendations. This lets you complete UI/auth/database testing before connecting Gemini.

## Test
`pytest -q`

## API docs
`http://127.0.0.1:8000/docs`

## Important data-source note
The project documentation asks for third-party platform sourcing and also allows mock/simulated calls. This version intentionally uses a mock catalog and platform search links instead of scraping sites without authorization. It does not claim that prices or availability are live.

## Main architecture
`Frontend → FastAPI routes → Gemini service → structured recommendations → SQLite history → Jinja2 result UI`


Party Planner and Jewelry Planner include guaranteed demo-fallback handling when Gemini is not configured.
