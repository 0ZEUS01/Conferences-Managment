from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import *
from auth import *
import pyodbc


app = FastAPI()

auth_handler = AuthHandler()
# Connect to SQL Server
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=127.0.0.1;"
    "Database=GC;"
    "UID=zeus;"
    "PWD=zeus;"
)
# Configure CORS
origins = ["*"]  # Set your allowed origins here
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/Nationality")
def get_Nationalities():
    cursor = conn.cursor()
    cursor.execute("SELECT country_id,country_name  FROM Country")
    rows = cursor.fetchall()

    Nationalities = []

    for row in rows:
        country_data = {
            "country_id": row[0],
            "country_name": row[1]
        }
        Nationalities.append(country_data)

    return {"Nationality": Nationalities}


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
