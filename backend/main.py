from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import pyodbc
from model import *
from auth import *
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
import threading

app = FastAPI()
auth_handler = AuthHandler()
lock = threading.Lock()

# Connect to SQL Server
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=127.0.0.1;"
    "Database=GC;"
    "UID=zeus;"
    "PWD=zeus;"
)

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/country")
def get_countries():
    with lock:
        try:
            cursorCountries = conn.cursor()
            cursorCountries.execute("SELECT country_id, country_name FROM Country")
            rows = cursorCountries.fetchall()

            countries = []

            for row in rows:
                country_data = {
                    "country_id": row[0],
                    "country_name": row[1]
                }
                countries.append(country_data)

            return {"country": countries}

        finally:
            cursorCountries.close()


@app.get("/state")
def get_state():
    with lock:
        try:
            cursorState = conn.cursor()
            cursorState.execute("SELECT state_conference_id, state_conference_name FROM State_conference")
            rows = cursorState.fetchall()

            states = []

            for row in rows:
                state_data = {
                    "state_conference_id": row[0],
                    "state_conference_name": row[1]
                }
                states.append(state_data)

            return {"state": states}

        finally:
            cursorState.close()


@app.get("/get_conference")
def get_conference():
    with lock:
        try:
            cursorConference = conn.cursor()
            cursorConference.execute("SELECT Co.title, C.country_name, Co.start_date, Co.end_date, Co.min_participants, Co.max_participants, S.state_conference_name, Co.address, Co.organizer_id,Co.conference_id FROM Conference Co JOIN Country C ON Co.country=C.country_id JOIN State_conference S ON CO.state_conference_id=S.state_conference_id")
            rows = cursorConference.fetchall()

            conferences = []

            for row in rows:
                conference_data = {
                    "title": row[0],
                    "country_name": row[1],
                    "start_date": row[2],
                    "end_date": row[3],
                    "min_participants": row[4],
                    "max_participants": row[5],
                    "state_conference_name": row[6],
                    "Address": row[7],
                    "organizer_id": row[8],
                    "conference_id": row[9]
                }
                conferences.append(conference_data)

            return {"conference": conferences}

        finally:
            cursorConference.close()

@app.get("/get_Completedconferences")
def get_conference():
    with lock:
        try:
            cursorConference = conn.cursor()
            cursorConference.execute("SELECT Co.title, C.country_name, Co.start_date, Co.end_date, Co.min_participants, Co.max_participants, S.state_conference_name, Co.address, Co.organizer_id,Co.conference_id FROM Conference Co JOIN Country C ON Co.country=C.country_id JOIN State_conference S ON CO.state_conference_id=S.state_conference_id WHERE S.state_conference_name='COMPLETED'")
            rows = cursorConference.fetchall()

            conferences = []

            for row in rows:
                conference_data = {
                    "title": row[0],
                    "country_name": row[1],
                    "start_date": row[2],
                    "end_date": row[3],
                    "min_participants": row[4],
                    "max_participants": row[5],
                    "state_conference_name": row[6],
                    "Address": row[7],
                    "organizer_id": row[8],
                    "conference_id": row[9]
                }
                conferences.append(conference_data)

            return {"conference": conferences}

        finally:
            cursorConference.close()

@app.get("/get_Endedconferences")
def get_conference():
    with lock:
        try:
            cursorConference = conn.cursor()
            cursorConference.execute("SELECT Co.title, C.country_name, Co.start_date, Co.end_date, Co.min_participants, Co.max_participants, S.state_conference_name, Co.address, Co.organizer_id,Co.conference_id FROM Conference Co JOIN Country C ON Co.country=C.country_id JOIN State_conference S ON CO.state_conference_id=S.state_conference_id WHERE S.state_conference_name='ENDED'")
            rows = cursorConference.fetchall()

            conferences = []

            for row in rows:
                conference_data = {
                    "title": row[0],
                    "country_name": row[1],
                    "start_date": row[2],
                    "end_date": row[3],
                    "min_participants": row[4],
                    "max_participants": row[5],
                    "state_conference_name": row[6],
                    "Address": row[7],
                    "organizer_id": row[8],
                    "conference_id": row[9]
                }
                conferences.append(conference_data)

            return {"conference": conferences}

        finally:
            cursorConference.close()

@app.get("/get_Canceledconferences")
def get_conference():
    with lock:
        try:
            cursorConference = conn.cursor()
            cursorConference.execute("SELECT Co.title, C.country_name, Co.start_date, Co.end_date, Co.min_participants, Co.max_participants, S.state_conference_name, Co.address, Co.organizer_id,Co.conference_id FROM Conference Co JOIN Country C ON Co.country=C.country_id JOIN State_conference S ON CO.state_conference_id=S.state_conference_id WHERE S.state_conference_name='CANCELED'")
            rows = cursorConference.fetchall()

            conferences = []

            for row in rows:
                conference_data = {
                    "title": row[0],
                    "country_name": row[1],
                    "start_date": row[2],
                    "end_date": row[3],
                    "min_participants": row[4],
                    "max_participants": row[5],
                    "state_conference_name": row[6],
                    "Address": row[7],
                    "organizer_id": row[8],
                    "conference_id": row[9]
                }
                conferences.append(conference_data)

            return {"conference": conferences}

        finally:
            cursorConference.close()

@app.post("/register")
async def register(user: Users_Register):
    try:
        cursor = conn.cursor()

        # Check if the email is already registered
        cursor.execute(
            "SELECT COUNT(*) FROM Users WHERE email = ? OR username = ?",
            (user.email, user.username)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="Email or username already registered"
            )

        # Insert the user into the Users table
        cursor.execute(
            """
            INSERT INTO Users (first_name, last_name, email, phone_number, username, password, birthdate, Address, nationality, picture)
            OUTPUT inserted.*
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
                user.Address,
                user.nationality,
                user.picture,
            ),
        )
        user_id = cursor.fetchone()[0]  # Fetch the user_id

        # Insert the user_id into the Participant table
        cursor.execute(
            "INSERT INTO Participant (user_id) VALUES (?)",
            (user_id,),
        )
        conn.commit()
        return {"message": "User registered successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database error1')


@app.post("/login")
async def login(u: Users_Login):
    try:
        cursor = conn.cursor()
        # Check if the email and password match a user in the database
        print(u)
        cursor.execute(
            """
            SELECT u.user_id, u.first_name, u.last_name, u.email, u.phone_number, u.username, u.password, u.birthdate, u.Address, c.country_name, u.picture, u.isAdmin,
            'Role' = (CASE
                WHEN EXISTS (SELECT 1 FROM Participant WHERE user_id = u.user_id) THEN 'Participant'
                ELSE ''
            END) +
            (CASE
                WHEN EXISTS (SELECT 1 FROM Searcher WHERE user_id = u.user_id) THEN (CASE WHEN 'Role' = '' THEN '' ELSE 'And' END) + 'Searcher'
                ELSE ''
            END) +
            (CASE
                WHEN EXISTS (SELECT 1 FROM Organizer WHERE user_id = u.user_id) THEN (CASE WHEN 'Role' = '' THEN '' ELSE 'And' END) + 'Organizer'
                ELSE ''
            END) +
            (CASE
                WHEN EXISTS (SELECT 1 FROM Protractor WHERE user_id = u.user_id) THEN (CASE WHEN 'Role' = '' THEN '' ELSE 'And' END) + 'Protractor'
                ELSE ''
            END)
            FROM Users u
            JOIN Country c ON u.nationality = c.country_id
            WHERE (u.username = ? OR u.email = ?)
            """,
            (u.usernameOrEmail, u.usernameOrEmail)
        )
        result = cursor.fetchone()
        if result is None or not auth_handler.verify_password(u.password, result.password):
            raise HTTPException(
                status_code=401, detail="Invalid email or username or password"
            )

        token = auth_handler.encode_token(result[0])
        return {
            "user_id": result[0],
            "access_token": token,
            "token_type": "bearer",
            "first_name": result[1],
            "last_name": result[2],
            "birthdate": result[7],
            "username": result[5],
            "email": result[3],
            "Address": result[8],
            "phone_number": result[4],
            "picture": result[10],
            "isAdmin": result[11],
            "Role": result[12],
            "nationality": result[9],
        }
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail="Database error2")


@app.post("/create_conference")
async def create_conference(c: Add_conference):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Conference WHERE title = ?",
            (c.title)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="A conference with same title already registered"
            )

        cursor.execute(
            """
                INSERT INTO Conference (title, country, address, min_participants, max_participants, organizer_id, start_date, state_conference_id, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, 3, ?)
            """,
            (
                c.title,
                c.country,
                c.address,
                c.min_participants,
                c.max_participants,
                c.organizer_id,
                c.start_date,
                c.end_date,
            ),
        )

        conn.commit()
        return {"message": "Conference registered successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database error')


@app.post("/edit_conference")
async def edit_conference(conference: Edit_conference):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Conference WHERE conference_id = ?",
            (conference.conference_id,),
        )
        if cursor.fetchone()[0] == 0:
            raise HTTPException(
                status_code=404, detail="Conference not found"
            )
        cursor.execute(
            """
                UPDATE Conference
                SET title=?, country=?, address=?, min_participants=?, max_participants=?,
                    organizer_id=?, start_date=?, state_conference_id=?, end_date=?
                WHERE conference_id=?
            """,
            (
                conference.title,
                conference.country,
                conference.address,
                conference.min_participants,
                conference.max_participants,
                conference.organizer_id,
                conference.start_date,
                conference.state_conference_id,
                conference.end_date,
                conference.conference_id,
            ),
        )

        conn.commit()
        return {"message": "Conference updated successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")

@app.post("/create_submissions")
async def create_submissions(c: Create_Submissions):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Article WHERE article_title = ?",
            (c.article_title)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="An Article with same title already registered"
            )

        cursor.execute(
            """
                INSERT INTO Article (article_title, article_content,searcher_id)
                VALUES (?, ?, ?)
                INSERT INTO Submission(submission_date, conference_id, article_id, report_id)
                VALUES(?, ?, ?, ?)
            """,
            (
                c.article_title,
                c.article_content,
                c.searcher_id,
                c.submission_date,
                c.conference_id,
                c.article_id,
                c.report_id,
            ),
        )

        conn.commit()
        return {"message": "Submission registered successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database error')


@app.delete("/delete_conference/{conferenceId}")
def delete_conference(conferenceId: int):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Conference WHERE conference_id = ?",
            (conferenceId,),
        )
        if cursor.fetchone()[0] == 0:
            raise HTTPException(
                status_code=404, detail="Conference not found"
            )

        cursor.execute(
            "DELETE FROM Conference WHERE conference_id = ?",
            (conferenceId,),
        )

        conn.commit()

        return {"message": f"Conference {conferenceId} deleted successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
