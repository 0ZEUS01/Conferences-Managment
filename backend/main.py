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
            cursorCountries.execute(
                "SELECT country_id, country_name FROM Country")
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
            cursorState.execute(
                "SELECT state_conference_id, state_conference_name FROM State_conference")
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


@app.get("/decision")
def get_decision():
    with lock:
        try:
            cursorDecision = conn.cursor()
            cursorDecision.execute(
                        "SELECT decision_id, decision FROM Decision")
            rows = cursorDecision.fetchall()

            decisions = []

            for row in rows:
                decision_data = {
                    "decision_id": row[0],
                    "decision": row[1]
                }
                decisions.append(decision_data)

            return {"decision": decisions}

        finally:
            cursorDecision.close()


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


@app.get("/get_Scheduledconferences")
def get_conference():
    with lock:
        try:
            cursorConference = conn.cursor()
            cursorConference.execute("SELECT Co.title, C.country_name, Co.start_date, Co.end_date, Co.min_participants, Co.max_participants, S.state_conference_name, Co.address, Co.organizer_id,Co.conference_id FROM Conference Co JOIN Country C ON Co.country=C.country_id JOIN State_conference S ON CO.state_conference_id=S.state_conference_id WHERE S.state_conference_name='SCHEDULED'")
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


@app.get("/get_Articles/{user_id}")
def get_Articles(user_id: int):
    with lock:
        try:
            cursorArticle = conn.cursor()
            cursorArticle.execute("""
                SELECT A.article_id, A.article_title, A.article_content, C.title, D.decision
                FROM Article A
                JOIN Submission S ON S.article_id = A.article_id
                JOIN Conference C ON C.conference_id = S.conference_id
                LEFT JOIN OrganizerDecision OD ON S.submission_id = OD.submission_id
                LEFT JOIN Decision D ON D.decision_id = OD.decision_id
                WHERE A.searcher_id = (SELECT searcher_id FROM Searcher WHERE user_id = ?)
            """, (user_id,))
            rows = cursorArticle.fetchall()

            articles = []

            for row in rows:
                conference_data = {
                    "article_id": row[0],
                    "article_title": row[1],
                    "article_content": row[2],
                    "title": row[3],
                    "decision": row[4],
                }
                articles.append(conference_data)

            return {"article": articles}

        finally:
            cursorArticle.close()


@app.get("/show_Articles")
def get_Articles():
    with lock:
        try:
            cursorArticle = conn.cursor()
            cursorArticle.execute("""
            SELECT A.article_id, A.article_title, A.article_content,C.conference_id, C.title, C.start_date, C.Address, Co.country_name,U.user_id,S.searcher_id, U.first_name, U.last_name FROM Article A JOIN Searcher S ON A.searcher_id=S.searcher_id Join Users U ON U.user_id=S.user_id
            JOIN Submission Su ON Su.article_id=A.article_id JOIN Conference C ON C.conference_id = Su.conference_id JOIN Country Co ON C.country = Co.country_id
            """)
            rows = cursorArticle.fetchall()

            articles = []

            for row in rows:
                Article_data = {
                    "article_id": row[0],
                    "article_title": row[1],
                    "article_content": row[2],
                    "conference_id": row[3],
                    "conference_title": row[4],
                    "start_date": row[5],
                    "address": row[6],
                    "country_name": row[7],
                    "user_id": row[8],
                    "searcher_id": row[9],
                    "first_name": row[10],
                    "last_name": row[11]
                }
                articles.append(Article_data)

            return {"article": articles}

        finally:
            cursorArticle.close()


@app.get("/show_Reports")
def get_reports():
    with lock:
        try:
            cursorReport = conn.cursor()
            cursorReport.execute("""
                SELECT R.report_id, R.report_content, U.first_name, U.last_name, C.title, A.article_title, A.article_content, D.decision,A.article_id FROM Report R
				JOIN ReportWrittenBy RW ON RW.report_id = R.report_id
				JOIN Protractor P ON P.protractor_id = RW.protractor_id
				JOIN Users U ON P.user_id = U.user_id
				JOIN Submission S ON S.report_id = R.report_id
				JOIN Conference C ON C.conference_id = S.conference_id
				JOIN Article A ON A.article_id = S.article_id
				LEFT JOIN OrganizerDecision OD ON S.submission_id = OD.submission_id
				LEFT JOIN Decision D ON D.decision_id = OD.decision_id
            """)
            rows = cursorReport.fetchall()

            reports = []

            for row in rows:
                report_data = {
                    "report_id": row[0],
                    "report_content": row[1],
                    "protractor_first_name": row[2],
                    "protractor_last_name": row[3],
                    "conference_title": row[4],
                    "article_title": row[5],
                    "article_content": row[6],
                    "decision": row[7],
                    "article_id": row[8]
                }
                reports.append(report_data)

            return {"report": reports}

        finally:
            cursorReport.close()

@app.get("/show_Approved_Reports")
def get_reports():
    with lock:
        try:
            cursorReport = conn.cursor()
            cursorReport.execute("""
                SELECT R.report_id, R.report_content, U.first_name, U.last_name, C.title, A.article_title, A.article_content, D.decision,A.article_id FROM Report R
				JOIN ReportWrittenBy RW ON RW.report_id = R.report_id
				JOIN Protractor P ON P.protractor_id = RW.protractor_id
				JOIN Users U ON P.user_id = U.user_id
				JOIN Submission S ON S.report_id = R.report_id
				JOIN Conference C ON C.conference_id = S.conference_id
				JOIN Article A ON A.article_id = S.article_id
				LEFT JOIN OrganizerDecision OD ON S.submission_id = OD.submission_id
				LEFT JOIN Decision D ON D.decision_id = OD.decision_id
                WHERE D.decision = 'APPROVED'
            """)
            rows = cursorReport.fetchall()

            reports = []

            for row in rows:
                report_data = {
                    "report_id": row[0],
                    "report_content": row[1],
                    "protractor_first_name": row[2],
                    "protractor_last_name": row[3],
                    "conference_title": row[4],
                    "article_title": row[5],
                    "article_content": row[6],
                    "decision": row[7],
                    "article_id": row[8]
                }
                reports.append(report_data)

            return {"report": reports}

        finally:
            cursorReport.close()

@app.get("/show_Refused_Reports")
def get_reports():
    with lock:
        try:
            cursorReport = conn.cursor()
            cursorReport.execute("""
                SELECT R.report_id, R.report_content, U.first_name, U.last_name, C.title, A.article_title, A.article_content, D.decision,A.article_id FROM Report R
				JOIN ReportWrittenBy RW ON RW.report_id = R.report_id
				JOIN Protractor P ON P.protractor_id = RW.protractor_id
				JOIN Users U ON P.user_id = U.user_id
				JOIN Submission S ON S.report_id = R.report_id
				JOIN Conference C ON C.conference_id = S.conference_id
				JOIN Article A ON A.article_id = S.article_id
				LEFT JOIN OrganizerDecision OD ON S.submission_id = OD.submission_id
				LEFT JOIN Decision D ON D.decision_id = OD.decision_id
                WHERE D.decision = 'REFUSED'
            """)
            rows = cursorReport.fetchall()

            reports = []

            for row in rows:
                report_data = {
                    "report_id": row[0],
                    "report_content": row[1],
                    "protractor_first_name": row[2],
                    "protractor_last_name": row[3],
                    "conference_title": row[4],
                    "article_title": row[5],
                    "article_content": row[6],
                    "decision": row[7],
                    "article_id": row[8]
                }
                reports.append(report_data)

            return {"report": reports}

        finally:
            cursorReport.close()


@app.get("/show_Reports/{user_id}")
def get_reports(user_id: int):
    with lock:
        try:
            cursorReport = conn.cursor()
            cursorReport.execute("""
                SELECT R.report_id, R.report_content, U.first_name, U.last_name, C.title, A.article_title, A.article_content, D.decision FROM Report R
				JOIN ReportWrittenBy RW ON RW.report_id = R.report_id
				JOIN Protractor P ON P.protractor_id = RW.protractor_id
				JOIN Users U ON P.user_id = U.user_id
				JOIN Submission S ON S.report_id = R.report_id
				JOIN Conference C ON C.conference_id = S.conference_id
				JOIN Article A ON A.article_id = S.article_id
				LEFT JOIN OrganizerDecision OD ON S.submission_id = OD.submission_id
				LEFT JOIN Decision D ON D.decision_id = OD.decision_id
                WHERE P.protractor_id = (SELECT protractor_id FROM Protractor WHERE user_id = ?)
            """, (user_id,))
            rows = cursorReport.fetchall()

            reports = []

            for row in rows:
                report_data = {
                    "report_id": row[0],
                    "report_content": row[1],
                    "protractor_first_name": row[2],
                    "protractor_last_name": row[3],
                    "conference_title": row[4],
                    "article_title": row[5],
                    "article_content": row[6],
                    "decision": row[7]
                }
                reports.append(report_data)

            return {"report": reports}

        finally:
            cursorReport.close()


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


@app.post("/create_submissions/{user_id}")
async def create_submissions(c: Create_Submissions, user_id: int):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Article WHERE article_title = ?",
            (c.article_title,)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="An Article with the same title is already registered"
            )

        cursor.execute(
            """
                SELECT searcher_id FROM Searcher WHERE user_id = ?
            """,
            (user_id,)
        )
        searcher_id = cursor.fetchone()[0]

        cursor.execute(
            """
                INSERT INTO Article (article_title, article_content, searcher_id)
                OUTPUT inserted.article_id
                VALUES (?, ?, ?)
            """,
            (c.article_title, c.article_content, searcher_id)
        )
        article_id = cursor.fetchone()[0]

        today = datetime.now().date()

        cursor.execute(
            """
                INSERT INTO Submission (submission_date, conference_id, article_id, report_id)
                VALUES (?, ?, ?, ?)
            """,
            (today, c.conference_id, article_id, None)
        )

        conn.commit()
        return {"message": "Submission registered successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/update_submissions1")
async def update_submissions(c: Searcher_Edit_Articles1):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Article WHERE article_title = ?",
            (c.article_title)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="An Article with same title already exist"
            )

        cursor.execute(
            """
                UPDATE Article SET article_title = ?, article_content = ?
                WHERE article_id = ?
            """,
            (
                c.article_title,
                c.article_content,
                c.article_id,
            ),
        )

        conn.commit()
        return {"message": "Article modified successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database error')


@app.post("/update_submissions2")
async def update_submissions(c: Searcher_Edit_Articles2):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Article WHERE article_title = ?",
            (c.article_title)
        )
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="An Article with same title already exist"
            )

        cursor.execute(
            """
                UPDATE Article SET article_title = ?
                WHERE article_id = ?
            """,
            (
                c.article_title,
                c.article_id,
            ),
        )

        conn.commit()
        return {"message": "Article modified successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database error')


@app.post("/create_report/{user_id}")
async def create_report(c: Create_Report, user_id: int):
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
		        INSERT INTO Report (report_content)
                OUTPUT inserted.report_id
                VALUES(?)
            """,
            (c.report_content,)
        )
        report_id = cursor.fetchone()[0]

        cursor.execute(
            """
                SELECT protractor_id FROM Protractor WHERE user_id = ?
            """,
            (user_id,)
        )
        protractor_id = cursor.fetchone()[0]

        cursor.execute(
            """
		        INSERT INTO ReportWrittenBy(protractor_id, report_id)
                VALUES (?, ?)
            """,
            (protractor_id, report_id,)
        )

        cursor.execute(
            """
		        UPDATE Submission
                SET report_id = ? WHERE article_id = ?
            """,
            (report_id, c.article_id,)
        )
        conn.commit()
        return {"message": "Report registered successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


@app.post("/edit_report")
async def update_report(c: Protractor_Edit_Report):
    try:
        cursor = conn.cursor()

        cursor.execute(
            """
                UPDATE Report SET report_content = ?
                WHERE report_id = ?
            """,
            (
                c.report_content,
                c.report_id,
            ),
        )

        conn.commit()
        return {"message": "Report modified successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail='Database error')

@app.post("/edit_Article_decision/{article_id}")
async def update_report(c: Article_decision, article_id: int):
    try:
        cursor = conn.cursor()

        cursor.execute(
            """SELECT submission_id FROM Submission WHERE article_id=?
            """,
            (article_id,),
        )
        submission_id = cursor.fetchone()[0]

        cursor.execute(
            """SELECT user_id FROM Organizer WHERE organizer_id =?
            """,
            (c.organizer_id,),
        )
        organizer = cursor.fetchone()[0]

        # Check if the OrganizerDecision already exists
        cursor.execute(
            """SELECT * FROM OrganizerDecision WHERE submission_id = ? AND organizer_id = ?;
            """,
            (submission_id,organizer),
        )
        existing_decision = cursor.fetchone()

        if existing_decision:
            # Update the existing OrganizerDecision
            cursor.execute(
                """UPDATE OrganizerDecision
                SET decision_id = ?
                WHERE submission_id = ?;
                """,
                (c.decision_id, submission_id),
            )
        else:
            # Insert a new OrganizerDecision
            cursor.execute(
                """INSERT INTO OrganizerDecision (organizer_id, submission_id, decision_id)
                VALUES (?, ?, ?);
                """,
                (organizer, submission_id, c.decision_id),
            )

        conn.commit()
        return {"message": "decision modified successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


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


@app.delete("/delete_submissions/{article_Id}")
def delete_submissions(article_Id: int):
    try:
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM Article WHERE article_id = ?",
            (article_Id,),
        )
        if cursor.fetchone()[0] == 0:
            raise HTTPException(
                status_code=404, detail="Article not found"
            )

        cursor.execute(
            "DELETE FROM Submission WHERE article_Id = ?",
            (article_Id,),
        )
        cursor.execute(
            "DELETE FROM Article WHERE article_Id = ?",
            (article_Id,),
        )

        conn.commit()

        return {"message": f"Article {article_Id} deleted successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


@app.delete("/delete_report/{report_id}")
def delete_submissions(report_id: int):
    try:
        print("Deleting report with report_id:", report_id)  # Debug statement

        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM report WHERE report_id = ?",
            (report_id,),
        )
        if cursor.fetchone()[0] == 0:
            raise HTTPException(
                status_code=404, detail="Report not found"
            )

        cursor.execute(
            """ UPDATE Submission
                SET report_id =NULL
                WHERE report_id = ?
            """,
            (report_id,),
        )
        cursor.execute(
            "DELETE FROM ReportWrittenBy WHERE report_id = ?",
            (report_id,),
        )
        cursor.execute(
            "DELETE FROM Report WHERE report_id = ?",
            (report_id,),
        )

        conn.commit()

        print("Report deleted successfully")  # Debug statement

        return {"message": f"Report {report_id} deleted successfully"}
    except pyodbc.Error as e:
        print(e)
        raise HTTPException(status_code=500, detail="Database error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
