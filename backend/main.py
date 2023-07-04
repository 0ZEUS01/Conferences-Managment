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
async def register(user: Users):
    try:
        cursor = conn.cursor()
        # Check if the email is already registered
        cursor.execute(
            "SELECT COUNT(*) FROM users WHERE email = ?", user.email)
        if cursor.fetchone()[0] > 0:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # Insert the user into the database
        cursor.execute(
            """
                INSERT INTO Users (first_name, last_name, email, phone_number, username, password, birthdate, Address, nationality, picture, isAdmin)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                user.isAdmin,
            ),
        )
        conn.commit()

        return {"message": "User registered successfully"}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail='Database error1')


@app.post("/login")
async def login(u: Users):
    try:
        cursor = conn.cursor()
        # Check if the email and password match a user in the database
        cursor.execute(
            """
            select u.user_id, u.first_name, u.last_name, u.email, u.phone_number, u.username ,u.password, u.birthdate, u.Address,c.country_name, u.picture, u.isAdmin ,'Role'= (case
					when u.user_id in (select user_id from Participant) then 'Participant'
					when u.user_id in (select user_id from Searcher) then 'Searcher'
					when u.user_id in (select user_id from Organizer) then 'Organizer'
					when u.user_id in (select user_id from Protractor) then 'Protractor'
					end)
					from Users u, Country c
                    WHERE (username = ? OR email = ?) AND u.nationality = c.country_id 
            """,
            (u.username, u.email)
        )
        result = cursor.fetchone()
        if result is None or not auth_handler.verify_password(u.password, result.password):
            raise HTTPException(
                status_code=401, detail="Invalid email or username or password ")

        token = auth_handler.encode_token(result[0])
        return {
            "user_id": result.user_id,
            "access_token": token,
            "token_type": "bearer",
            "first_name": result.first_name,
            "last_name": result.last_name,
            "birthdate": result.birthdate,
            "username": result.username,
            "email": result.email,
            "Address": result.Address,
            "phone_number": result.phone_number,
            "picture": result.picture,
            "isAdmin": result.isAdmin,
            "Role": result.Role,
            "nationality": result.country_name
        }
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail='Database error2')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
