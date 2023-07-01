from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import *
from auth import *
import pyodbc

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
    allow_origins=["http://localhost:3000"],  # Replace with the actual origin of your frontend app
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

@app.get("/countries")
def get_countries():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Country")
    rows = cursor.fetchall()

    countries = []

    for row in rows:
        country_data = {
            "country_id": row[0],
            "country_name": row[1],
            "iso": row[2]
        }
        countries.append(country_data)

    return countries


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

@app.get("/committees")
def get_committees():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Committee")
    rows = cursor.fetchall()

    committees = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        committee_data = dict(zip(columns, row))
        committees.append(committee_data)

    return {"committees": committees}

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

@app.get("/authors")
def get_authors():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Authors")
    rows = cursor.fetchall()

    authors = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        author_data = dict(zip(columns, row))
        authors.append(author_data)

    return {"authors": authors}

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

@app.get("/roles")
def get_roles():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Roles")
    rows = cursor.fetchall()

    roles = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        role_data = dict(zip(columns, row))
        roles.append(role_data)

    return {"roles": roles}

@app.get("/role_assignments")
def get_role_assignments():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM RoleAssignments")
    rows = cursor.fetchall()

    role_assignments = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        assignment_data = dict(zip(columns, row))
        role_assignments.append(assignment_data)

    return {"role_assignments": role_assignments}

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

@app.get("/accepted_submissions")
def get_accepted_submissions():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM AcceptedSubmissions")
    rows = cursor.fetchall()

    accepted_submissions = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        submission_data = dict(zip(columns, row))
        accepted_submissions.append(submission_data)

    return {"accepted_submissions": accepted_submissions}

@app.get("/sessions")
def get_sessions():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sessions")
    rows = cursor.fetchall()

    sessions = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        session_data = dict(zip(columns, row))
        sessions.append(session_data)

    return {"sessions": sessions}

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

@app.get("/registrations")
def get_registrations():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Registration")
    rows = cursor.fetchall()

    registrations   = []
    columns = [column[0] for column in cursor.description]

    for row in rows:
        registration_data = dict(zip(columns, row))
        registrations.append(registration_data)

    return {"registrations": registrations}

@app.post("/register")
async def register(user: Users_Register):
    try:
        cursor = conn.cursor()

        # Check if the username is already in use
        cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (user.username,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="Username already in use")

        # Check if the email is already registered
        cursor.execute("SELECT COUNT(*) FROM Users WHERE email = ?", (user.email,))
        if cursor.fetchone()[0] > 0:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Insert the user into the database
        cursor.execute(
            """
            INSERT INTO Users (first_name, last_name, email, username, password, birthdate, country)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user.first_name,
                user.last_name,
                user.email,
                user.username,
                auth_handler.get_password_hash(user.password),
                user.birthdate,
                user.country,
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
            raise HTTPException(status_code=401, detail="Invalid username, email, or password")

        user_id = result.user_id
        token = auth_handler.encode_token(user_id)

        return {"ID": user_id, "access_token": token, "token_type": "bearer"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail='Database error')

