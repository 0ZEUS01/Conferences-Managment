# 🎓 Conference Management System - FastAPI

This is a full-stack Conference Management System backend built with **FastAPI**. It allows users to register, submit articles, join conferences, and manage participation. Administrators and organizers can manage conferences, submissions, and make decisions on article reports. This system is backed by a comprehensive relational database in SQL Server.

---

## 📚 Table of Contents

- [🚀 Features](#-features)
- [🏗️ Project Structure](#-project-structure)
- [🛠️ Technologies Used](#-technologies-used)
- [🧠 Database Schema](#-database-schema)
- [📦 Installation](#-installation)
- [🧪 API Endpoints](#-api-endpoints)
- [📄 Reports and Documentation](#-reports-and-documentation)
- [🧑‍💻 Contributing](#-contributing)
- [📃 License](#-license)

---

## 🚀 Features

- 🔐 User authentication and registration
- 🌍 Multi-national support (users and conferences have countries)
- 📋 Article submission and management
- 📁 Report uploads by protractors
- 👩‍🏫 Organizer decision-making process
- 📊 Role-based functionalities: Admin, Organizer, Protractor, Searcher, Participant
- 📆 Conference management with min/max participants and scheduling
- 📥 Searcher and participant registration to conferences
- 📃 Binary file handling for articles and reports
- 🧩 Strongly relational SQL Server schema

---

## 🏗️ Project Structure

```
📁 app/
├── 📁 api/              # FastAPI route handlers
├── 📁 models/           # Pydantic and SQLAlchemy models
├── 📁 crud/             # Database interaction logic
├── 📁 core/             # Settings, configs, utilities
├── 📁 db/               # Database connection and init
├── main.py             # Entry point
📄 README.md
```

---

## 🛠️ Technologies Used

- **FastAPI** – High-performance Python API framework
- **SQLAlchemy** – ORM for database models
- **Pydantic** – Data validation
- **SQL Server** – Main relational database
- **Uvicorn** – ASGI server
- **Alembic** – Database migrations
- **JWT Auth** – Token-based security

---

## 🧠 Database Schema Overview

The system includes the following key tables:

- `Users` – Stores user data and roles
- `Country` – List of countries
- `Conference` – Core entity with title, location, dates
- `Participant`, `Searcher`, `Protractor`, `Organizer` – User role mappings
- `Article` – Submitted research
- `Report` – Files submitted by protractors
- `Submission` – Link between conferences and articles/reports
- `Decision` – Organizer's decisions
- `ParticipantInConference`, `SearcherJoinConference`, `ReportWrittenBy`, `OrganizerDecision` – Relationship tables

➡️ Full SQL schema is available in the `/docs/database.sql` file.

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/conference-management-fastapi.git
cd conference-management-fastapi
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env` or `settings.py`

```env
DATABASE_URL=mssql+pyodbc://<username>:<password>@localhost/GC?driver=ODBC+Driver+17+for+SQL+Server
SECRET_KEY=your_jwt_secret_key
```

### 5. Run the app

```bash
uvicorn main:app --reload
```

The API will be available at:  
📍 `http://127.0.0.1:8000`

Swagger UI: `http://127.0.0.1:8000/docs`

---

## 🧪 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register` | Register user |
| `POST` | `/auth/login` | Login and receive JWT |
| `GET`  | `/conferences/` | List all conferences |
| `POST` | `/conferences/` | Create new conference |
| `POST` | `/articles/submit` | Submit an article |
| `POST` | `/reports/` | Upload report (Protractors) |
| `POST` | `/submissions/{id}/decision` | Organizer makes decision |
| `GET`  | `/users/me` | Get current user profile |

🧪 Explore more using `/docs`

---

## 📄 Reports and Documentation

This repo includes:

- 📘 `Project_Report.pdf` – Full project documentation
- 🧬 `Conception/` – Contains UML diagrams, use cases, and class design
- 🗂 `docs/database.sql` – Full SQL Server schema
- 📊 ER Diagram: [`er_diagram.png`](docs/er_diagram.png)

---

## 🧑‍💻 Contributing

Contributions are welcome! To contribute:

1. Fork the repo
2. Create a new branch (`git checkout -b feature-name`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push (`git push origin feature-name`)
5. Open a pull request 🎉

---

## 📃 License

This project is licensed under the MIT License.  
See [`LICENSE`](LICENSE) for more information.

---

## 📞 Contact

For any inquiries or support, contact us at:

📧 zini.yahya22@gmail.com  
📍 GitHub: [@0ZEUS01](https://github.com/0ZEUS01)

---

> Built with ❤️ using FastAPI
```
