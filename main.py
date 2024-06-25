import sqlite3
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from database import init_db, get_db_connection
from datetime import datetime

app = FastAPI()
templates = Jinja2Templates(directory="templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.mount("/static", StaticFiles(directory="static"), name="static")

init_db()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    conn = get_db_connection()
    tools = conn.execute('SELECT * FROM tools').fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "tools": tools})

@app.get("/login.html", response_class=HTMLResponse)
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "return_url": "/"})

@app.get("/cadastro.html", response_class=HTMLResponse)
def cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request, "return_url": "/"})

@app.post("/users/")
def create_user(
    full_name: str = Form(...),
    address: str = Form(...),
    cpf: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
    is_manager: bool = Form(False)
):
    hashed_password = pwd_context.hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (full_name, address, cpf, password, email, is_manager)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (full_name, address, cpf, hashed_password, email, is_manager))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="CPF or email already registered")
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/tools/")
def create_tool(name: str = Form(...), description: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tools (name, description, available)
    VALUES (?, ?, ?)
    ''', (name, description, True))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)

@app.post("/rentals/")
def create_rental(client_id: int = Form(...), tool_id: int = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO rentals (request_date, status, client_id, tool_id)
    VALUES (?, ?, ?, ?)
    ''', (datetime.utcnow(), "em análise", client_id, tool_id))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)
