from pydantic import BaseModel
from datetime import date

class Country(BaseModel):
    country_id: int
    country_Name: str

class Users_Register(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    username: str
    password: str
    birthdate: date
    Address: str
    nationality: int
    picture: bytes

class Users_Login(BaseModel):
    usernameOrEmail: str
    password: str


class State(BaseModel):
    state_id: int
    state_name: str

class Organizer(BaseModel):
    organizer_id: int
    user_id: int

class Add_conference(BaseModel):
    title: str
    address: str
    start_date: str
    end_date: str
    min_participants: int
    max_participants: int
    country: int
    state: int
    organizer_id: int

class Participant(BaseModel):
    participant_id: int
    user_id: int

class ParticipantInConference(BaseModel):
    participant_id: int
    conference_id: int

class Searcher(BaseModel):
    searcher_id: int
    user_id: int

class Articles(BaseModel):
    article_id: int
    article_title: str
    article_content: bytes
    searcher_id: int

class SearcherJoinConference(BaseModel):
    searcher_id: int
    conference_id: int
    article_id: int

class Protractor(BaseModel):
    protractor_id: int
    user_id: int

class Report(BaseModel):
    report_id: int
    report_content: bytes

class ReportWrittenBy(BaseModel):
    protractor_id: int
    report_id: int

class Submissions(BaseModel):
    submission_id: int
    submission_date: str
    conference_id: int
    article_id: int
    report_id: int

class Decision(BaseModel):
    decision_id: int
    decision: str

class OrganizerDecision(BaseModel):
    organizer_id: int
    submission_id: int
    decision_id: int




