from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from model import *
from auth import *
import pyodbc
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

auth_handler = AuthHandler()
# Connect to SQL Server
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=127.0.0.1;"
    "Database=GC;"
    "UID=zeus;"
    "PWD=zeus;"
)
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Replace with the actual origin of your frontend app
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="../frontend/admin")

@app.post("/register")
async def register(user: Users_Register):
    try:
        cursor = conn.cursor()

        # Check if the username is already in use
        cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE username = ?", (user.username,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="Username already in use")

        # Check if the email is already registered
        cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE email = ?", (user.email,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # Insert the user into the database
        cursor.execute(
            """
            INSERT INTO Users (first_name, last_name, email, phone_number, username, password, birthdate, address, nationality, picture)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.first_name,
                user.last_name,
                user.email,
                user.phone_number,
                user.username,
                auth_handler.get_password_hash(user.password),
                user.birthdate,
                user.address,
                user.nationality,
                user.picture,
            ),
        )
        conn.commit()

        return {"message": "User registered successfully"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/login")
async def login(u: Users_Login):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, password FROM Users WHERE email = ? OR username = ?",
            (u.usernameOrEmail, u.usernameOrEmail),
        )
        result = cursor.fetchone()
        if result is None or not auth_handler.verify_password(u.password, result.password):
            raise HTTPException(
                status_code=401, detail="Invalid username, email, or password")

        user_id = result.user_id
        token = auth_handler.encode_token(user_id)

        return {"ID": user_id, "access_token": token, "token_type": "bearer"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail='Database error')

@app.get("/Nationality", response_class=HTMLResponse)
def get_Nationalities(request: Request):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Country")
    rows = cursor.fetchall()

    Nationalities = []

    for row in rows:
        country_data = {
            "country_id": row[0],
            "country_name": row[1],
            "iso": row[2]
        }
        Nationalities.append(country_data)

    return templates.TemplateResponse("register.html", {"request": request, "Nationalities": Nationalities})


@app.get("/state_conference")
def get_states():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM State_conference")
    rows = cursor.fetchall()

    states_conference = []

    for row in rows:
        state_conference_data = {
            "state_conference_id": row[0],
            "state_conference_name": row[1]
        }
        states_conference.append(state_conference_data)

    return states_conference


@app.get("/decision")
def get_decisions():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Decision")
    rows = cursor.fetchall()

    decisions = []

    for row in rows:
        decision_data = {
            "decision_id": row[0],
            "decision": row[1]
        }
        decisions.append(decision_data)

    return decisions


@app.get("/conferences")
def get_conferences():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Conference")
    rows = cursor.fetchall()

    conferences = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        conference_data = dict(zip(columns, row))
        conferences.append(conference_data)

    return {"conferences": conferences}


@app.get("/submissions")
def get_submissions():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Submissions")
    rows = cursor.fetchall()

    submissions = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        submission_data = dict(zip(columns, row))
        submissions.append(submission_data)

    return {"submissions": submissions}

@app.get("/users")
def get_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users")
    rows = cursor.fetchall()

    users = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        user_data = dict(zip(columns, row))
        users.append(user_data)

    return {"users": users}


@app.get("/reports")
def get_reports():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Reports")
    rows = cursor.fetchall()

    reports = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        report_data = dict(zip(columns, row))
        reports.append(report_data)

    return {"reports": reports}


@app.get("/articles")
def get_articles():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Articles")
    rows = cursor.fetchall()

    articles = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        article_data = dict(zip(columns, row))
        articles.append(article_data)

    return {"articles": articles}


