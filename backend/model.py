from pydantic import BaseModel

class Country(BaseModel):
    country_id: int
    country_Name: str
    ISO: str

class Conference(BaseModel):
    conference_id: int
    title: str
    country: int
    address: str
    start_date: str
    end_date: str
    min_participants: int
    max_participants: int

class Committee(BaseModel):
    committee_id: int
    conference: int
    organizer_name: str

class Submissions(BaseModel):
    submission_id: int
    conference: int
    submission_date: str
    document: str

class Authors(BaseModel):
    author_id: int
    submission: int
    author_name: str

class Users_Login(BaseModel):
    usernameOrEmail: str
    password: str

class Users_Register(BaseModel):
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    birthdate: str
    country: int


class Users(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    birthdate: str
    country: int
    isAdmin: bool
    
class Roles(BaseModel):
    role_id: int
    role_name: str

class RoleAssignments(BaseModel):
    assignment_id: int
    conference: int
    role_id: int
    user_id: int

class Reports(BaseModel):
    report_id: int
    assignment_id: int
    submission_id: int
    rating: int
    report_text: str

class AcceptedSubmissions(BaseModel):
    accepted_submission_id: int
    conference: int
    submission: int

class Sessions(BaseModel):
    session_id: int
    conference_id: int
    session_title: str
    session_date: str
    start_time: str
    end_time: str
    session_type: str

class Articles(BaseModel):
    article_id: int
    submission_id: int
    article_text: str


